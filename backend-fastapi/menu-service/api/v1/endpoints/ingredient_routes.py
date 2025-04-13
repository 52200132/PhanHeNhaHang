from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.sesstion import get_db
from schemas.ingredient_schemas import IngredientCreate, IngredientUpdate, IngredientResponse
from crud.ingredient_crud import add_ingredient, get_ingredient, update_ingredient, delete_ingredient, get_all_ingredients

router = APIRouter()

# Thêm nguyên liệu vào menu
@router.post("/ingredients/", response_model=IngredientResponse)
def create_new_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    new_ingredient = add_ingredient(db=db, ingredient=ingredient)
    return new_ingredient

# Lấy tất cả nguyên liệu trong menu
@router.get("/ingredients/", response_model=list[IngredientResponse])
def read_all_ingredients(db: Session = Depends(get_db)):
    ingredients = get_all_ingredients(db=db)
    return ingredients

# Lấy từng nguyên liệu trong menu
@router.get("/ingredients/{ingredient_id}", response_model=IngredientResponse)
def read_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = get_ingredient(db=db, ingredient_id=ingredient_id)
    return ingredient

# Cập nhật thông tin nguyên liệu trong menu
@router.patch("/ingredients/{ingredient_id}", response_model=IngredientResponse)
def update_existing_ingredient(ingredient_id: int, ingredient: IngredientUpdate, db: Session = Depends(get_db)):
    updated_ingredient = update_ingredient(db=db, ingredient_id=ingredient_id, ingredient=ingredient)
    return updated_ingredient

# Xóa nguyên liệu trong menu
@router.delete("/ingredients/{ingredient_id}")
def delete_existing_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    deleted_ingredient = delete_ingredient(db=db, ingredient_id=ingredient_id)
    return {"message": "Ingredient deleted successfully"}