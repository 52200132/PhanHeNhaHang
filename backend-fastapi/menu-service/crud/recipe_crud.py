from sqlalchemy.orm import Session
from models.models import Recipe
from schemas.recipe_schemas import RecipeCreate, RecipeUpdate, RecipeResponse
from fastapi import HTTPException

def add_recipe(db: Session, recipe: RecipeCreate):
    db_recipe = Recipe(
        dish_id=recipe.dish_id,
        ingredient_id=recipe.ingredient_id,
        unit=recipe.unit,
        base_amount=recipe.base_amount
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return RecipeResponse.from_orm(db_recipe)

def get_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return RecipeResponse.from_orm(db_recipe)

def update_recipe(db: Session, recipe_id: int, recipe: RecipeUpdate):
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    for key, value in recipe.dict(exclude_unset=True).items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return RecipeResponse.from_orm(db_recipe)

def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return {"detail": "Recipe deleted successfully"}