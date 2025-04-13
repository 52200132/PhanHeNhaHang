from sqlalchemy.orm import Session
from models.models import Recipe
from schemas.recipe_schemas import RecipeCreate, RecipeUpdate, RecipeResponse
from fastapi import HTTPException

# C
# Thêm công thức vào menu
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
# R
# Lấy tất cả công thức trong menu
def get_all_recipes(db: Session):
    db_recipes = db.query(Recipe).all()
    if not db_recipes:
        raise HTTPException(status_code=404, detail="No recipes found")
    return {
        "message": "Recipes retrieved successfully",
        "data": [RecipeResponse.from_orm(recipe) for recipe in db_recipes]
    }
# Lấy công thức (món ăn) theo ID
def get_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id} not found")
    return RecipeResponse.from_orm(db_recipe)

# Lấy công thức (món ăn) theo nguyên liệu => có được danh sách món ăn có nguyên liệu đó
def get_recipe_by_ingredient(db: Session, ingredient_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.ingredient_id == ingredient_id).all()
    if not db_recipe:
        raise HTTPException(status_code=404, detail=f"No recipes found for ingredient ID {ingredient_id}")
    return {
        "message": "Recipes retrieved successfully",
        "data": [RecipeResponse.from_orm(recipe) for recipe in db_recipe]
    }

# U
# Cập nhật thông tin công thức trong menu
def update_recipe(db: Session, recipe_id: int, recipe: RecipeUpdate):
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id} not found")
    for key, value in recipe.dict(exclude_unset=True).items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return RecipeResponse.from_orm(db_recipe)
# D
# Xóa công thức trong menu
def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(Recipe).filter(Recipe.recipe_id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail=f"Recipe with ID {recipe_id} not found")
    db.delete(db_recipe)
    db.commit()
    return {"detail": "Recipe deleted successfully"}