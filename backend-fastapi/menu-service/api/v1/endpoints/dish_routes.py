from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.sesstion import get_db
from schemas.dish_schemas import DishCreate, DishUpdate, DishResponse
from crud.dish_crud import add_dish, get_dish, update_dish, delete_dish, get_all_dish, get_all_dish_by_category

router = APIRouter()

# Thêm món ăn vào menu
@router.post("/dishes/", response_model=DishResponse)
def create_new_dish(dish: DishCreate, db: Session = Depends(get_db)):
    new_dish = add_dish(db=db, dish=dish)
    return new_dish

# Lấy tất cả món ăn trong menu
@router.get("/dishes/", response_model=list[DishResponse])
def read_all_dishes(db: Session = Depends(get_db)):
    dishes = get_all_dish(db=db)
    return dishes

# Lấy tất cả món ăn có liên quan đến loại món ăn
@router.get("/dishes/categories/{category_id}", response_model=list[DishResponse])
def read_all_dishes_by_category(category_id: int, db: Session = Depends(get_db)):
    dishes = get_all_dish_by_category(db=db, category_id=category_id)
    return dishes

# Lấy thông tin từng món ăn trong menu
@router.get("/dishes/{dish_id}", response_model=DishResponse)
def read_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = get_dish(db=db, dish_id=dish_id)
    return dish

# Cập nhật thông tin món ăn trong menu
@router.patch("/dishes/{dish_id}", response_model=DishResponse)
def update_existing_dish(dish_id: int, dish: DishUpdate, db: Session = Depends(get_db)):
    updated_dish = update_dish(db=db, dish_id=dish_id, dish=dish)
    return updated_dish

# Xóa món ăn trong menu
@router.delete("/dishes/{dish_id}")
def delete_existing_dish(dish_id: int, db: Session = Depends(get_db)):
    deleted_dish = delete_dish(db=db, dish_id=dish_id)
    return {"message": "Dish deleted successfully"}