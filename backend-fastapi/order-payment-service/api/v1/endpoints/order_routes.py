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

@router.post("/orders/add-orderdetails/{order_id}")
def add_orderdetais_to_order(
    order_id: int,
    order_details: list[OrderDetail],
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
        order_details = [OrderDetailCreate(**item.dict()) for item in order_details]
        add_dish = order_crud.add_order_details(db, order_id, order_details)
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

@router.patch("/orders/{order_id}")
def update_order_status(
    order_id: int,
    status: str = "Hoàn thành",
    db: Session = Depends(get_db),
):
    try:
        # Cập nhật trạng thái đơn hàng
        order = order_crud.update_order_status(db, order_id, status)
        return {
            "message": "Order status updated successfully",
            "success": True,
            "data": order,
        }
    except Exception as e:
        logger.error(f"Error updating order status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )