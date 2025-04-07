from sqlalchemy.orm import Session
from models.models import Ingredient
from schemas.ingredient_schemas import IngredientCreate, IngredientUpdate, IngredientResponse
from fastapi import HTTPException

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

def get_ingredient(db: Session, ingredient_id: int):
    db_ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return IngredientResponse.from_orm(db_ingredient)

def update_ingredient(db: Session, ingredient_id: int, ingredient: IngredientUpdate):
    db_ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    for key, value in ingredient.dict(exclude_unset=True).items():
        setattr(db_ingredient, key, value)
    db.commit()
    db.refresh(db_ingredient)
    return IngredientResponse.from_orm(db_ingredient)

def delete_ingredient(db: Session, ingredient_id: int):
    db_ingredient = db.query(Ingredient).filter(Ingredient.ingredient_id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db.delete(db_ingredient)
    db.commit()
    return {"detail": "Ingredient deleted successfully"}