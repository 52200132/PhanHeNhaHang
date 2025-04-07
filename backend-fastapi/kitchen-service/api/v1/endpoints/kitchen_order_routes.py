from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.sesstion import get_db
from schemas.kitchen_order_schemas import KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse
from crud.kitchen_order_crud import add_kitchen_order, get_kitchen_order, update_kitchen_order, delete_kitchen_order

router = APIRouter()

@router.post("/kitchen_orders/")
def create_kitchen_order(kitchen_order: KitchenOrderCreate, db: Session = Depends(get_db)):
    return add_kitchen_order(db=db, kitchen_order=kitchen_order)