from sqlalchemy.orm import Session
from models.models import KitchenOrder
from schemas.kitchen_order_schemas import KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse
from fastapi import HTTPException
from utils.logger import get_logger

# Create logger for this module
logger = get_logger(__name__)

# Thêm đơn hàng vào bếp
def add_kitchen_order(db: Session, kitchen_order: KitchenOrderCreate):
    logger.info(f"Adding new kitchen order for order_id: {kitchen_order.order_id}, dish_id: {kitchen_order.dish_id}")
    try:
        db_kitchen_order = KitchenOrder(
            order_id=kitchen_order.order_id,
            dish_id=kitchen_order.dish_id,
            status=kitchen_order.status,
            note=kitchen_order.note,
            quantity=kitchen_order.quantity,
            create_at=kitchen_order.create_at
        )
        db.add(db_kitchen_order)
        db.commit()
        db.refresh(db_kitchen_order)
        logger.debug(f"Kitchen order created with ID: {db_kitchen_order.kitchen_order_id}")
        return KitchenOrderResponse.from_orm(db_kitchen_order)
    except Exception as e:
        logger.error(f"Error adding kitchen order: {str(e)}")
        raise

# Lấy tất cả đơn hàng trong bếp
def get_all_kitchen_orders(db: Session):
    logger.info("Getting all kitchen orders")
    try:
        db_kitchen_orders = db.query(KitchenOrder).all()
        if not db_kitchen_orders:
            logger.warning("No kitchen orders found")
            raise HTTPException(status_code=404, detail="No kitchen orders found")
        logger.debug(f"Retrieved {len(db_kitchen_orders)} kitchen orders")
        return {
            "message": "Kitchen orders retrieved successfully",
            "data": [KitchenOrderResponse.from_orm(order) for order in db_kitchen_orders]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving kitchen orders: {str(e)}")
        raise

# Lấy tất cả đơn hàng trong bếp theo trạng thái
def get_kitchen_orders_by_status(db: Session, status: str):
    logger.info(f"Getting kitchen orders with status: {status}")
    try:
        db_kitchen_orders = db.query(KitchenOrder).filter(KitchenOrder.status == status).all()
        if not db_kitchen_orders:
            logger.warning(f"No kitchen orders found with status {status}")
            raise HTTPException(status_code=404, detail=f"No kitchen orders found with status {status}")
        logger.debug(f"Retrieved {len(db_kitchen_orders)} kitchen orders with status {status}")
        return {
            "message": "Kitchen orders retrieved successfully",
            "data": [KitchenOrderResponse.from_orm(order) for order in db_kitchen_orders]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving kitchen orders by status: {str(e)}")
        raise

# Lấy từng đơn hàng trong bếp
def get_kitchen_order(db: Session, kitchen_order_id: int):
    logger.info(f"Getting kitchen order with ID: {kitchen_order_id}")
    try:
        db_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.kitchen_order_id == kitchen_order_id).first()
        if not db_kitchen_order:
            logger.warning(f"Kitchen order with ID {kitchen_order_id} not found")
            raise HTTPException(status_code=404, detail=f"Kitchen order with ID {kitchen_order_id} not found")
        logger.debug(f"Retrieved kitchen order with ID: {kitchen_order_id}")
        return KitchenOrderResponse.from_orm(db_kitchen_order)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving kitchen order: {str(e)}")
        raise

# Câp nhật đơn hàng trong bếp
def update_kitchen_order(db: Session, kitchen_order_id: int, kitchen_order: KitchenOrderUpdate):
    logger.info(f"Updating kitchen order with ID: {kitchen_order_id}")
    try:
        db_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.kitchen_order_id == kitchen_order_id).first()
        if not db_kitchen_order:
            logger.warning(f"Kitchen order with ID {kitchen_order_id} not found for update")
            raise HTTPException(status_code=404, detail=f"Kitchen order with ID {kitchen_order_id} not found")
        for key, value in kitchen_order.dict(exclude_unset=True).items():
            setattr(db_kitchen_order, key, value)
        db.commit()
        db.refresh(db_kitchen_order)
        logger.debug(f"Kitchen order with ID {kitchen_order_id} updated successfully")
        return KitchenOrderResponse.from_orm(db_kitchen_order)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating kitchen order: {str(e)}")
        raise

# Xóa đơn hàng trong bếp
def delete_kitchen_order(db: Session, kitchen_order_id: int):
    logger.info(f"Deleting kitchen order with ID: {kitchen_order_id}")
    try:
        db_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.kitchen_order_id == kitchen_order_id).first()
        if not db_kitchen_order:
            logger.warning(f"Kitchen order with ID {kitchen_order_id} not found for deletion")
            raise HTTPException(status_code=404, detail=f"Kitchen order with ID {kitchen_order_id} not found")
        db.delete(db_kitchen_order)
        db.commit()
        logger.debug(f"Kitchen order with ID {kitchen_order_id} deleted successfully")
        return {"detail": "Kitchen order deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting kitchen order: {str(e)}")
        raise