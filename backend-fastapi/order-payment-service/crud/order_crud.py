from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime 
from httpx import AsyncClient

from utils.logger import get_logger
from schemas.order_schemas import MakeOrder, OrderStatus, OrderResonpense
from schemas.orderdetail_schemas import OrderDetailCreate, OrderDetailResponse
from models.models import Table, Order
from crud import orderdetail_crud, fetch_data
from redis_stream.producer import redis_producer
from redis_stream.config import ORDER_CREATED_STREAM


logger = get_logger(__name__)


async def create_order(db: AsyncSession, order: MakeOrder):
    """
    Tạo đơn hàng với danh sách món ăn
    """
    try:
        # Kiểm tra xem bàn có tồn tại không
        query = select(Table).filter(Table.table_id == order.table_id)
        result = await db.execute(query)
        table = result.scalars().first()
        if not table:
            logger.error(f"Table not found: {order.table_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        table_status ="available" if table.is_available == True else "busy"
        
        # TODO: Nếu table đang bận

        # Tạo đơn hàng
        db_order = Order(
            table_id = order.table_id,
            checkIn_time = datetime.now(),
            checkOut_time = datetime.now(),
            total_price = 1,
            is_paid = False,
            status = OrderStatus.cho_xu_ly
        )
        db.add(db_order)
        await db.commit()
        await db.refresh(db_order)

        # Tính tổng giá cho đơn hàng
        for item in order.items:
            item.order_id = db_order.order_id
        order_items =  await orderdetail_crud.create_list_order_detail(db, order.items)
        db_order.total_price = sum(item.total_price for item in order_items)
        logger.info(f"Total price calculated: {db_order.total_price}")
        await db.commit()
        await db.refresh(db_order)

        # TODO: Publish sự kiện hoàn tạo đơn hàng lên Redis
        redis_data = OrderResonpense.from_orm(db_order)
        redis_producer.produce_message(
            stream=ORDER_CREATED_STREAM,
            data=redis_data
        )
        
        logger.info(f"Order created: {db_order.order_id}")
        return {
            "order": OrderResonpense.from_orm(db_order),
            "order_items": order_items,
        }
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error when creating order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def get_order_by_id(db: AsyncSession, order_id: int):
    """
        Lấy thông tin đơn hàng theo order_id
        {
            "order": OrderResonpense,
            "order_items": List[OrderDetailResponse]
        }
    """
    try:
        query = select(Order).options(selectinload(Order.order_details)).filter(Order.order_id == order_id)
        result = await db.execute(query)
        order = result.scalars().first()
        if not order:
            logger.error(f"Order not found: {order_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        # Lấy danh sách món ăn trong đơn hàng
        order_items = order.order_details

        logger.info(f"Order retrieved: {order.order_id}")
        return {
            "order": OrderResonpense.from_orm(order),
            "order_items": [OrderDetailResponse.from_orm(item) for item in order_items],
        }
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error when retrieving order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as e:
        await db.rollback()
        logger.error(f"Error retrieving order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def add_order_detail(db: AsyncSession, order_id: int, order_detail: OrderDetailCreate):
    """
    Thêm món ăn vào đơn hàng
    """
    try:
        # Kiểm tra xem đơn hàng có tồn tại không
        query = select(Order).filter(Order.order_id == order_id).options(selectinload(Order.order_details))
        result = await db.execute(query)
        order = result.scalars().first()
        if not order:
            logger.error(f"Order not found: {order_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        

        # Thêm món ăn vào đơn hàng
        order_detail.order_id = order.order_id
        order_items = await orderdetail_crud.create_list_order_detail(db, [order_detail])
        
        # Cập nhật tổng giá cho đơn hàng
        await db.refresh(order)
        order.total_price = sum(item.total_price for item in order.order_details if not item.is_deleted)
        await db.commit()
        await db.refresh(order)

        logger.info(f"Dish added to order: {order.order_id}")
        return OrderResonpense.from_orm(order)
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error when adding dish to order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def delete_order_detail(db: AsyncSession, order_detail_id: int):
    """
        Xóa món ăn trong đơn hàng
    """
    try:
        order_detail = await orderdetail_crud.delete_order_detail(db, order_detail_id)
        if not order_detail:
            logger.error(f"Order detail not found: {order_detail_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order detail not found")
        # Cập nhật tổng giá cho đơn hàng
        query = select(Order).filter(Order.order_id == order_detail.order_id).options(selectinload(Order.order_details))
        result = await db.execute(query)
        order = result.scalars().first()
        order.total_price = sum(item.total_price for item in order.order_details if not item.is_deleted)
        await db.commit()
        await db.refresh(order)

        logger.info(f"Dish deleted from order: {order.order_id}")
        return {
            "order": OrderResonpense.from_orm(order),
            "order_detail_deleted": order_detail
        }
    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Integrity error when deleting dish from order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))