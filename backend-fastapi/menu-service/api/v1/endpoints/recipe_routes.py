from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.sesstion import get_db
from schemas.recipe_schemas import RecipeCreate, RecipeUpdate, RecipeResponse
from crud.recipe_crud import add_recipe, get_recipe, update_recipe, delete_recipe, get_all_recipes, get_recipe_by_ingredient

router = APIRouter()

# Thêm công thức vào menu
@router.post("/recipes/", response_model=RecipeResponse)
def create_new_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = add_recipe(db=db, recipe=recipe)
    return new_recipe
# Lấy tất cả công thức trong menu
@router.get("/recipes/", response_model=list[RecipeResponse])
def read_all_recipes(db: Session = Depends(get_db)):
    recipes = get_all_recipes(db=db)
    return recipes
# Lấy từng công thức trong menu
@router.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_recipe(db=db, recipe_id=recipe_id)
    return recipe
#Lấy công thức (món ăn) theo nguyên liệu => có được danh sách món ăn có nguyên liệu đó
@router.get("/recipes/ingredient/{ingredient_id}", response_model=list[RecipeResponse])
def read_recipe_by_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    recipes = get_recipe_by_ingredient(db=db, ingredient_id=ingredient_id)
    return recipes
# Cập nhật thông tin công thức trong menu
@router.patch("/recipes/{recipe_id}", response_model=RecipeResponse)
def update_existing_recipe(recipe_id: int, recipe: RecipeUpdate, db: Session = Depends(get_db)):
    updated_recipe = update_recipe(db=db, recipe_id=recipe_id, recipe=recipe)
    return updated_recipe
# Xóa công thức trong menu
@router.delete("/recipes/{recipe_id}")
def delete_existing_recipe(recipe_id: int, db: Session = Depends(get_db)):
    deleted_recipe = delete_recipe(db=db, recipe_id=recipe_id)
    return {"message": "Recipe deleted successfully"}