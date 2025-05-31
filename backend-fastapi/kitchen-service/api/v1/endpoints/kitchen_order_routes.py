from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.sesstion import get_db
from schemas.kitchen_order_schemas import KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse
from crud.kitchen_order_crud import add_kitchen_order, get_kitchen_order, update_kitchen_order, delete_kitchen_order, get_all_kitchen_orders, get_kitchen_orders_by_status
import httpx
from utils.logger import get_logger

# Create logger for this module
logger = get_logger(__name__)

router = APIRouter()

# Thêm đơn hàng vào bếp
@router.post("/kitchen_orders/")
def create_kitchen_order(kitchen_order: KitchenOrderCreate, db: Session = Depends(get_db)):
    logger.info(f"API request: Create kitchen order for order_id {kitchen_order.order_id}")
    try:
        new_kitchen_order = add_kitchen_order(db=db, kitchen_order=kitchen_order)
        logger.info(f"Kitchen order created successfully with ID: {new_kitchen_order.kitchen_order_id}")
        return new_kitchen_order
    except Exception as e:
        logger.error(f"Failed to create kitchen order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create kitchen order: {str(e)}")

# Xem tất cả đơn hàng trong bếp
@router.get("/kitchen_orders/")
def read_all_kitchen_orders(db: Session = Depends(get_db)):
    logger.info("API request: Get all kitchen orders")
    try:
        kitchen_orders = get_all_kitchen_orders(db=db)
        logger.info(f"Retrieved {len(kitchen_orders)} kitchen orders")
        return kitchen_orders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get kitchen orders: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get kitchen orders: {str(e)}")

# Xem tất cả đơn hàng trong bếp theo trạng thái
    # "Chưa chuẩn bị"
    # "Đang chế biến"
    # "Hoàn thành"
@router.get("/kitchen_orders/status/{status}")
def read_kitchen_orders_by_status(status: str, db: Session = Depends(get_db)):
    logger.info(f"API request: Get kitchen orders by status {status}")
    try:
        kitchen_orders = get_kitchen_orders_by_status(db=db, status=status)
        logger.info(f"Retrieved {len(kitchen_orders)} kitchen orders with status {status}")
        return kitchen_orders
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get kitchen orders by status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get kitchen orders by status: {str(e)}")

# Xem thông tin từng đơn hàng trong bếp
@router.get("/kitchen_orders/{kitchen_order_id}/")
def read_kitchen_order(kitchen_order_id: int, db: Session = Depends(get_db)):
    logger.info(f"API request: Get kitchen order with ID {kitchen_order_id}")
    try:
        kitchen_order = get_kitchen_order(db=db, kitchen_order_id=kitchen_order_id)
        logger.info(f"Retrieved kitchen order with ID {kitchen_order_id}")
        return kitchen_order
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get kitchen order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get kitchen order: {str(e)}")

# Chỉnh sửa (trạng thái) đơn hàng trong bếp
@router.patch("/kitchen_orders/{kitchen_order_id}/")
def update_existing_kitchen_order(kitchen_order_id: int, kitchen_order: KitchenOrderUpdate, db: Session = Depends(get_db)):
    logger.info(f"API request: Update kitchen order with ID {kitchen_order_id}")
    try:
        updated_kitchen_order = update_kitchen_order(db=db, kitchen_order_id=kitchen_order_id, kitchen_order=kitchen_order)
        logger.info(f"Kitchen order with ID {kitchen_order_id} updated successfully")
        return updated_kitchen_order
    except Exception as e:
        logger.error(f"Failed to update kitchen order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update kitchen order: {str(e)}")

# Xóa đơn hàng trong bếp
@router.delete("/kitchen_orders/{kitchen_order_id}/")
def delete_existing_kitchen_order(kitchen_order_id: int, db: Session = Depends(get_db)):
    logger.info(f"API request: Delete kitchen order with ID {kitchen_order_id}")
    try:
        deleted_kitchen_order = delete_kitchen_order(db=db, kitchen_order_id=kitchen_order_id)
        logger.info(f"Kitchen order with ID {kitchen_order_id} deleted successfully")
        return deleted_kitchen_order
    except Exception as e:
        logger.error(f"Failed to delete kitchen order: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete kitchen order: {str(e)}")

# Menu Service port: 8000
# Order Payment Service port: 8001
# Kitchen Service port: 8002

# Call Menu Service to get dish details

# Xem tất cả món ăn trong menu
@router.get("/call-menu-service/dishes/")
async def get_all_dish():
    logger.info("API request: Calling menu service to get all dishes")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8001/api/v1/dishes/")
            logger.info("Successfully retrieved dishes from menu service")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to call menu service: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Menu service unavailable: {str(e)}")

# Lấy tất cả loại món ăn trong menu
@router.get("/call-menu-service/categories/")
async def get_all_categories():
    logger.info("API request: Calling menu service to get all categories")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8001/api/v1/categories/")
            logger.info("Successfully retrieved categories from menu service")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to call menu service: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Menu service unavailable: {str(e)}")

# Lấy tất cả món ăn có liên quan đến loại món ăn
@router.get("/call-menu-service/dishes/categories/{category_id}")
async def get_all_dish_by_category(category_id: int):
    logger.info(f"API request: Calling menu service to get dishes by category ID {category_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8001/api/v1/dishes/categories/{category_id}")
            logger.info(f"Successfully retrieved dishes for category ID {category_id} from menu service")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to call menu service: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Menu service unavailable: {str(e)}")

# Lấy tất cả công thức có liên quan đến nguyên liệu => có danh sách món có nguyên liệu đó
@router.get("/call-menu-service/recipes/ingredient/{ingredient_id}")
async def get_all_recipes_by_ingredient(ingredient_id: int):
    logger.info(f"API request: Calling menu service to get recipes by ingredient ID {ingredient_id}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8001/api/v1/recipes/ingredient/{ingredient_id}")
            logger.info(f"Successfully retrieved recipes for ingredient ID {ingredient_id} from menu service")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to call menu service: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Menu service unavailable: {str(e)}")

# Tắt món ăn trong menu 
@router.patch("/call-menu-service/turn-off-dish/{id}")
async def turn_off_available_status(id: int):
    logger.info(f"API request: Calling menu service to turn off dish ID {id}")
    body_data = {
        "is_available": False
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"http://localhost:8001/api/v1/dishes/{id}", json=body_data)
            logger.info(f"Successfully turned off dish ID {id} in menu service")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to call menu service: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Menu service unavailable: {str(e)}")

# Bật món ăn trong menu 
@router.patch("/call-menu-service/turn-on-dish/{id}")
async def turn_on_available_status(id: int):
    logger.info(f"API request: Calling menu service to turn on dish ID {id}")
    body_data = {
        "is_available": True
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"http://localhost:8001/api/v1/dishes/{id}", json=body_data)
            logger.info(f"Successfully turned on dish ID {id} in menu service")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to call menu service: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Menu service unavailable: {str(e)}")

# Call Order Payment Service to get order details
# in_process
@router.patch("/call-order-payment-service/orders/{id}")
async def switch_in_process_status(id: int):
    logger.info(f"API request: Calling order payment service to switch order ID {id} to in-process status")
    body_data = {
        "status": "Đang chế biến"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"http://localhost:8002/api/v1/orders/{id}", json=body_data)
            logger.info(f"Successfully switched order ID {id} to in-process status in order payment service")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to call order payment service: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Order payment service unavailable: {str(e)}")

# complete
@router.patch("/call-order-payment-service/orders/{id}")
async def switch_complete_status(id: int):
    logger.info(f"API request: Calling order payment service to switch order ID {id} to complete status")
    body_data = {
        "status": "Hoàn thành"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(f"http://localhost:8002/api/v1/orders/{id}?status=Hoàn thành", json=body_data)
            logger.info(f"Successfully switched order ID {id} to complete status in order payment service")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to call order payment service: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Order payment service unavailable: {str(e)}")