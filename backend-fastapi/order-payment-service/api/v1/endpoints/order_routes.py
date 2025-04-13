from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas import MakeOrder, ServiceResponseModel
from schemas.orderdetail_schemas import OrderDetailCreate, OrderDetail
from db.session import get_db
from utils.logger import get_logger
from crud import order_crud

logger = get_logger(__name__)

router = APIRouter(prefix="", tags=["orders"])


@router.post("/orders")
def create_order(order: MakeOrder, db: Session = Depends(get_db)):
    """
    MakeOrder: {
        table_id: int,
        items: List[OrderItem]
    }
    Mẫu JSON:
    {
        "table_id": 2,
        "items": [
            {
            "dish_id": 10,
            "quantity": 1
            },
            {
            "dish_id": 11,
            "quantity": 2,
            "note": "Cay nhiều"
            }
        ]
    }
    """
    try:
        # return(order)
        create_order = order_crud.create_order(db, order)
        return {
            "message": "Order created successfully",
            "success": True,
            "data": create_order,
        }

    except Exception as e:
        logger.error(f"Error creating order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/orders/{order_id}")
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
):
    try:
        # Lấy thông tin đơn hàng theo order_id
        order = order_crud.get_order_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {
            "message": "Order retrieved successfully",
            "success": True,
            "data": order,
        }
    except Exception as e:
        logger.error(f"Error retrieving order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

@router.post("/orders/add_orderdetail/{order_id}")
def add_orderdetai_to_order(
    order_id: int,
    order_detail: list[OrderDetail],
    db: Session = Depends(get_db),
):
    """
    [
        {
            "dish_id": 10,
            "quantity": 1,
            "note": "Ngon lắm" 
        },
        {
            "dish_id": 11,
            "quantity": 2,
            "note": "Cay nhiều"
        },
        {
            "dish_id": 12,
            "quantity": 3
        }
    ]
    """
    try:
        # Thêm món ăn vào đơn hàng
        order_detail = OrderDetailCreate(**order_detail.dict())
        add_dish = order_crud.add_order_detail(db, order_id, order_detail)
        return {
            "message": "Dish added to order successfully",
            "success": True,
            "data": add_dish,
        }
    except Exception as e:
        logger.error(f"Error adding dish to order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    

@router.delete("/orders/delete_orderdetail/{order_detail_id}")
def delete_orderdetail_from_order(
    order_detail_id: int,
    db: Session = Depends(get_db),
):
    try:
        # Xóa món ăn trong đơn hàng
        order_detail = order_crud.delete_order_detail(db, order_detail_id)
        return {
            "message": "OrderDetail deleted from order successfully",
            "success": True,
            "data": order_detail,
        }
    except Exception as e:
        logger.error(f"Error deleting dish from order: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )