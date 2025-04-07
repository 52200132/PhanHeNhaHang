from sqlalchemy.orm import Session
from models.models import KitchenOrder
from schemas.kitchen_order_schemas import KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse
from fastapi import HTTPException

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

def get_kitchen_order(db: Session, kitchen_order_id: int):
    db_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.kitchen_order_id == kitchen_order_id).first()
    if not db_kitchen_order:
        raise HTTPException(status_code=404, detail="Kitchen order not found")
    return KitchenOrderResponse.from_orm(db_kitchen_order)

def update_kitchen_order(db: Session, kitchen_order_id: int, kitchen_order: KitchenOrderUpdate):
    db_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.kitchen_order_id == kitchen_order_id).first()
    if not db_kitchen_order:
        raise HTTPException(status_code=404, detail="Kitchen order not found")
    for key, value in kitchen_order.dict(exclude_unset=True).items():
        setattr(db_kitchen_order, key, value)
    db.commit()
    db.refresh(db_kitchen_order)
    return KitchenOrderResponse.from_orm(db_kitchen_order)

def delete_kitchen_order(db: Session, kitchen_order_id: int):
    db_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.kitchen_order_id == kitchen_order_id).first()
    if not db_kitchen_order:
        raise HTTPException(status_code=404, detail="Kitchen order not found")
    db.delete(db_kitchen_order)
    db.commit()
    return {"detail": "Kitchen order deleted successfully"}