from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from schemas.orderdetail_schemas import OrderDetailCreate, OrderDetailResponse 
from models.models import OrderDetail
from utils.logger import get_logger
from httpx import Client
from crud.fetch_data import get_dish_price
from crud import call_service_api

logger = get_logger(__name__)

def create_list_order_detail(db: Session, order_detail_items: list[OrderDetailCreate]) -> OrderDetail:
    try:
        logger.info("Bắt đầu tạo order detail")
        # Lấy giá của dish_id từ database thông qua route api/v1/dishes/{dish_id}
        with Client() as client:
            for order_detail in order_detail_items:
                dish_price = get_dish_price(client, order_detail.dish_id)
                order_detail.total_price = dish_price * order_detail.quantity

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
        db.commit()
        # Cập nhật lại thông tin cho từng order_detail
        for order_detail in order_detail_list:
            db.refresh(order_detail)
            # Gọi API để tạo đơn hàng trong bếp
            call_service_api.call_create_kitchen_order_api(
                order_id=order_detail.order_id,
                dish_id=order_detail.dish_id,
                note=order_detail.note,
                quantity=order_detail.quantity
            )
        logger.info(f"Order details created successfully for order_id: {order_detail_items[0].order_id if order_detail_items else 'unknown'}")
        return [OrderDetailResponse.from_orm(orderdetail) for orderdetail in order_detail_list]
    except Exception as e:
        logger.error(f"Error creating order detail: {e}")
        db.rollback()
        raise e

def delete_order_detail(db: Session, order_detail_id: int):
    """
        Xóa món ăn trong đơn hàng
    """
    try:
        order_detail = db.query(OrderDetail).filter(OrderDetail.orderDetail_id == order_detail_id).first()
        if not order_detail:
            logger.error(f"Order detail not found: {order_detail_id}")
            return None
        order_detail.is_deleted = True  # Đánh dấu là đã xóa
        db.commit()
        db.refresh(order_detail)  # Cập nhật lại thông tin
        logger.info(f"Order detail deleted successfully: {order_detail_id}")
        return OrderDetailResponse.from_orm(order_detail)  # Trả về chi tiết đơn hàng đã xóa
    except Exception as e:
        logger.error(f"Error deleting order detail: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )