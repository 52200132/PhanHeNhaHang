from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import datetime 
from httpx import Client

from utils.logger import get_logger
from schemas.order_schemas import MakeOrder, OrderStatus, OrderResonpense
from schemas.orderdetail_schemas import OrderDetailCreate, OrderDetailResponse
from models.models import Table, Order, OrderDetail
from crud import orderdetail_crud, fetch_data

logger = get_logger(__name__)

def create_order(db: Session, order: MakeOrder):
    """
    Tạo đơn hàng với danh sách món ăn
    """
    try:
        # Kiểm tra xem bàn có tồn tại không
        table = db.query(Table).filter(Table.table_id == order.table_id).first()
        if not table:
            logger.error(f"Table not found: {order.table_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        table_status = "available" if table.is_available == True else "busy"
        
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
        db.commit()
        db.refresh(db_order)

        # Tính tổng giá cho đơn hàng
        for item in order.items:
            item.order_id = db_order.order_id
        order_items = orderdetail_crud.create_list_order_detail(db, order.items)
        db_order.total_price = sum(item.total_price for item in order_items)
        logger.info(f"Total price calculated: {db_order.total_price}")
        db.commit()
        db.refresh(db_order)
        
        logger.info(f"Order created: {db_order.order_id}")
        return {
            "order": OrderResonpense.from_orm(db_order),
            "order_items": order_items,
        }
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error when creating order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
def get_order_by_id(db: Session, order_id: int):
    """
        Lấy thông tin đơn hàng theo order_id
        {
            "order": OrderResonpense,
            "order_items": List[OrderDetailResponse]
        }
    """
    try:
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            logger.error(f"Order not found: {order_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        # Lấy danh sách món ăn trong đơn hàng
        order_items = db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()

        logger.info(f"Order retrieved: {order.order_id}")
        return {
            "order": OrderResonpense.from_orm(order),
            "order_items": [OrderDetailResponse.from_orm(item) for item in order_items],
        }
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error when retrieving order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as e:
        db.rollback()
        logger.error(f"Error retrieving order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def add_order_detail(db: Session, order_id: int, order_detail: OrderDetailCreate):
    """
    Thêm món ăn vào đơn hàng
    """
    try:
        # Kiểm tra xem đơn hàng có tồn tại không
        order = db.query(Order).filter(Order.order_id == order_id).first()
        if not order:
            logger.error(f"Order not found: {order_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        # Thêm món ăn vào đơn hàng
        order_detail.order_id = order.order_id
        order_items = orderdetail_crud.create_list_order_detail(db, [order_detail])
        
        # Cập nhật tổng giá cho đơn hàng
        order_details = db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()
        order.total_price = sum(item.total_price for item in order_details if not hasattr(item, 'is_deleted') or not item.is_deleted)
        db.commit()
        db.refresh(order)

        logger.info(f"Dish added to order: {order.order_id}")
        return OrderResonpense.from_orm(order)
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error when adding dish to order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
def delete_order_detail(db: Session, order_detail_id: int):
    """
        Xóa món ăn trong đơn hàng
    """
    try:
        order_detail = orderdetail_crud.delete_order_detail(db, order_detail_id)
        if not order_detail:
            logger.error(f"Order detail not found: {order_detail_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order detail not found")
        
        # Cập nhật tổng giá cho đơn hàng
        order = db.query(Order).filter(Order.order_id == order_detail.order_id).first()
        order_details = db.query(OrderDetail).filter(OrderDetail.order_id == order_detail.order_id).all()
        order.total_price = sum(item.total_price for item in order_details if not hasattr(item, 'is_deleted') or not item.is_deleted)
        db.commit()
        db.refresh(order)

        logger.info(f"Dish deleted from order: {order.order_id}")
        return {
            "order": OrderResonpense.from_orm(order),
            "order_detail_deleted": order_detail
        }
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error when deleting dish from order: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Integrity error")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))