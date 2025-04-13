from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.sesstion import get_db
from schemas.kitchen_order_schemas import KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse
from crud.kitchen_order_crud import add_kitchen_order, get_kitchen_order, update_kitchen_order, delete_kitchen_order, get_all_kitchen_orders, get_kitchen_orders_by_status
import httpx

router = APIRouter()

# Thêm đơn hàng vào bếp
@router.post("/kitchen_orders/")
def create_kitchen_order(kitchen_order: KitchenOrderCreate, db: Session = Depends(get_db)):
    new_kitchen_order = add_kitchen_order(db=db, kitchen_order=kitchen_order)
    return new_kitchen_order

# Xem tất cả đơn hàng trong bếp
@router.get("/kitchen_orders/", response_model=list[KitchenOrderResponse])
def read_all_kitchen_orders(db: Session = Depends(get_db)):
    kitchen_orders = get_all_kitchen_orders(db=db)
    return kitchen_orders

# Xem tất cả đơn hàng trong bếp theo trạng thái
    # "Chưa chuẩn bị"
    # "Đang chế biến"
    # "Hoàn thành"
@router.get("/kitchen_orders/status/{status}", response_model=list[KitchenOrderResponse])
def read_kitchen_orders_by_status(status: str, db: Session = Depends(get_db)):
    kitchen_orders = get_kitchen_orders_by_status(db=db, status=status)
    return kitchen_orders

# Xem thông tin từng đơn hàng trong bếp
@router.get("/kitchen_orders/{kitchen_order_id}/", response_model=KitchenOrderResponse)
def read_kitchen_order(kitchen_order_id: int, db: Session = Depends(get_db)):
    kitchen_order = get_kitchen_order(db=db, kitchen_order_id=kitchen_order_id)
    return kitchen_order

# Chỉnh sửa (trạng thái) đơn hàng trong bếp
@router.patch("/kitchen_orders/{kitchen_order_id}/")
def update_existing_kitchen_order(kitchen_order_id: int, kitchen_order: KitchenOrderUpdate, db: Session = Depends(get_db)):
    updated_kitchen_order = update_kitchen_order(db=db, kitchen_order_id=kitchen_order_id, kitchen_order=kitchen_order)
    return updated_kitchen_order

# Xóa đơn hàng trong bếp
@router.delete("/kitchen_orders/{kitchen_order_id}/")
def delete_existing_kitchen_order(kitchen_order_id: int, db: Session = Depends(get_db)):
    deleted_kitchen_order = delete_kitchen_order(db=db, kitchen_order_id=kitchen_order_id)
    return deleted_kitchen_order


# Menu Service port: 8000
# Order Payment Service port: 8001
# Kitchen Service port: 8002


# Call Menu Service to get dish details

# Xem tất cả món ăn trong menu
@router.get("/call-menu-service/dishes/")
async def get_all_dish():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/v1/dishes/")
        return response.json()

# Lấy tất cả loại món ăn trong menu
@router.get("/call-menu-service/categories/")
async def get_all_categories():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/v1/categories/")
        return response.json()
# Lấy tất cả món ăn có liên quan đến loại món ăn
@router.get("/call-menu-service/dishes/categories/{category_id}")
async def get_all_dish_by_category(category_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/api/v1/dishes/categories/{category_id}")
        return response.json()
    
# Lấy tất cả công thức có liên quan đến nguyên liệu => có danh sách món có nguyên liệu đó
@router.get("/call-menu-service/recipes/ingredient/{ingredient_id}")
async def get_all_recipes_by_ingredient(ingredient_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://localhost:8000/api/v1/recipes/ingredient/{ingredient_id}")
        return response.json()

# Tắt món ăn trong menu 
@router.patch("/call-menu-service/turn-off-dish/{id}")
async def turn_off_available_status(id: int):
    body_data = {
        "is_available": False
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(f"http://localhost:8000/api/v1/dishes/{id}", json=body_data)  # truyền phần body ở đây
        return response.json()

# Bật món ăn trong menu 
@router.patch("/call-menu-service/turn-on-dish/{id}")
async def turn_on_available_status(id: int):
    body_data = {
        "is_available": True
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(f"http://localhost:8000/api/v1/dishes/{id}", json=body_data)  # truyền phần body ở đây
        return response.json()

# Call Order Payment Service to get order details
# in_process
@router.patch("/call-order-payment-service/orders/{id}")
async def switch_in_process_status(id: int):
    body_data = {
        "status": "Đang chế biến"
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(f"http://localhost:8001/api/v1/orders/{id}", json=body_data)  # truyền phần body ở đây
        return response.json()
#complete
@router.patch("/call-order-payment-service/orders/{id}")
async def switch_complete_status(id: int):
    body_data = {
        "status": "Hoàn thành"
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(f"http://localhost:8001/api/v1/orders/{id}", json=body_data)  # truyền phần body ở đây
        return response.json()