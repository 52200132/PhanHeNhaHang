from sqlalchemy.orm import Session
from models.models import Ingredient
from schemas.ingredient_schemas import IngredientCreate, IngredientUpdate, IngredientResponse
from fastapi import HTTPException

# C
# Thêm nguyên liệu vào menu
def add_ingredient(db: Session, ingredient: IngredientCreate):
    db_ingredient = Ingredient(
        name=ingredient.name,
        quantity=ingredient.quantity,
        unit=ingredient.unit
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return IngredientResponse.from_orm(db_ingredient)
# R
# Lấy tất cả nguyên liệu trong menu
def get_all_ingredients(db: Session):
    db_ingredients = db.query(Ingredient).all()
    if not db_ingredients:
        raise HTTPException(status_code=404, detail="No ingredients found")
    return [IngredientResponse.from_orm(ingredient) for ingredient in db_ingredients]
# Lấy thông tin từng nguyên liệu trong menu
def get_ingredient(db: Session, ingredient_id: int):
    db_ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail=f"Ingredient with ID {ingredient_id} not found")
    return IngredientResponse.from_orm(db_ingredient)

# U
# Cập nhật thông tin nguyên liệu trong menu
def update_ingredient(db: Session, ingredient_id: int, ingredient: IngredientUpdate):
    db_ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail=f"Ingredient with ID {ingredient_id} not found")
    for key, value in ingredient.dict(exclude_unset=True).items():
        setattr(db_ingredient, key, value)
    db.commit()
    db.refresh(db_ingredient)
    return IngredientResponse.from_orm(db_ingredient)
# D
# Xóa nguyên liệu trong menu
def delete_ingredient(db: Session, ingredient_id: int):
    db_ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail=f"Ingredient with ID {ingredient_id} not found")
    db.delete(db_ingredient)
    db.commit()
    return {"detail": "Ingredient deleted successfully"}