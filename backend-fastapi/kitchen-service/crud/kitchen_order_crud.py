from sqlalchemy.orm import Session
from models.models import KitchenOrder
from schemas.kitchen_order_schemas import KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse
from fastapi import HTTPException

# Thêm đơn hàng vào bếp
def add_kitchen_order(db: Session, kitchen_order: KitchenOrderCreate):
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
    return KitchenOrderResponse.from_orm(db_kitchen_order)

# Lấy tất cả đơn hàng trong bếp
def get_all_kitchen_orders(db: Session):
    db_kitchen_orders = db.query(KitchenOrder).all()
    if not db_kitchen_orders:
        raise HTTPException(status_code=404, detail="No kitchen orders found")
    return {
        "message": "Kitchen orders retrieved successfully",
        "data": [KitchenOrderResponse.from_orm(order) for order in db_kitchen_orders]
    }

# Lấy tất cả đơn hàng trong bếp theo trạng thái
def get_kitchen_orders_by_status(db: Session, status: str):
    db_kitchen_orders = db.query(KitchenOrder).filter(KitchenOrder.status == status).all()
    if not db_kitchen_orders:
        raise HTTPException(status_code=404, detail=f"No kitchen orders found with status {status}")
    return {
        "message": "Kitchen orders retrieved successfully",
        "data": [KitchenOrderResponse.from_orm(order) for order in db_kitchen_orders]
    }

# Lấy từng đơn hàng trong bếp
def get_kitchen_order(db: Session, kitchen_order_id: int):
    db_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.kitchen_order_id == kitchen_order_id).first()
    if not db_kitchen_order:
        raise HTTPException(status_code=404, detail=f"Kitchen order with ID {kitchen_order_id} not found")
    return KitchenOrderResponse.from_orm(db_kitchen_order)

# Câp nhật đơn hàng trong bếp
def update_kitchen_order(db: Session, kitchen_order_id: int, kitchen_order: KitchenOrderUpdate):
    db_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.kitchen_order_id == kitchen_order_id).first()
    if not db_kitchen_order:
        raise HTTPException(status_code=404, detail=f"Kitchen order with ID {kitchen_order_id} not found")
    for key, value in kitchen_order.dict(exclude_unset=True).items():
        setattr(db_kitchen_order, key, value)
    db.commit()
    db.refresh(db_kitchen_order)
    return KitchenOrderResponse.from_orm(db_kitchen_order)

# Xóa đơn hàng trong bếp
def delete_kitchen_order(db: Session, kitchen_order_id: int):
    db_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.kitchen_order_id == kitchen_order_id).first()
    if not db_kitchen_order:
        raise HTTPException(status_code=404, detail=f"Kitchen order with ID {kitchen_order_id} not found")
    db.delete(db_kitchen_order)
    db.commit()
    return {"detail": "Kitchen order deleted successfully"}