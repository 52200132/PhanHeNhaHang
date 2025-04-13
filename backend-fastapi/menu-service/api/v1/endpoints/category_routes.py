from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.sesstion import get_db
from schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from crud.category_crud import add_category, get_category, update_category, delete_category


router = APIRouter()

# Thêm loại món ăn vào menu
@router.post("/categories/")
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    add_category(db=db, category=category)
    return {"message": "Category created successfully"}