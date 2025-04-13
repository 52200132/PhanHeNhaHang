from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy import select

from schemas.orderdetail_schemas import OrderDetailCreate, OrderDetailResponse 
from models.models import OrderDetail
from utils.logger import get_logger
from httpx import AsyncClient
from crud.fetch_data import get_dish_price

logger = get_logger(__name__)

async def create_list_order_detail(db: AsyncSession, order_detail_items: list[OrderDetailCreate]) -> OrderDetail:
    try:
        logger.info("Bat đầu tạo order detail")
        # Lấy giá của dish_id từ database thông qua route api/v1/dishes/{dish_id}
        async with AsyncClient() as client:
            for order_detail in order_detail_items:
                dish_price = await get_dish_price(client, order_detail.dish_id)
                order_detail.total_price = dish_price * order_detail.quantity
        

        # logger.info(f"Lấy prices thành công")
        order_detail_list = []
        for order_detail in order_detail_items:
            new_order_detail = OrderDetail(
                order_id=order_detail.order_id,
                dish_id=order_detail.dish_id,
                quantity=order_detail.quantity,
                unit_price="VNĐ",
                total_price=order_detail.total_price,
                note=order_detail.note
            )
            order_detail_list.append(new_order_detail)
            db.add(new_order_detail)
        await db.commit()
        # Cập nhật lại thông tin cho từng order_detail
        for order_detail in order_detail_list:
            await db.refresh(order_detail)
        logger.info(f"Order details created successfully for order_id: {order_detail_items[0].order_id if order_detail_items else 'unknown'}")
        return [OrderDetailResponse.from_orm(orderdetail) for orderdetail in order_detail_list]    # Trả về toàn bộ danh sách chi tiết đơn hàng thay vì chỉ mục cuối cùng
    except Exception as e:
        logger.error(f"Error creating order detail: {e}")
        await db.rollback()
        raise e

async def delete_order_detail(db: AsyncSession, order_detail_id: int):
    """
        Xóa món ăn trong đơn hàng
    """
    try:
        query = select(OrderDetail).filter(OrderDetail.orderDetail_id == order_detail_id)
        result = await db.execute(query)
        order_detail = result.scalars().first()
        if not order_detail:
            logger.error(f"Order detail not found: {order_detail_id}")
            return None
        order_detail.is_deleted = True  # Đánh dấu là đã xóa
        await db.commit()
        await db.refresh(order_detail)  # Cập nhật lại thông tin
        logger.info(f"Order detail deleted successfully: {order_detail_id}")
        return OrderDetailResponse.from_orm(order_detail)  # Trả về chi tiết đơn hàng đã xóa
    except Exception as e:
        logger.error(f"Error deleting order detail: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )