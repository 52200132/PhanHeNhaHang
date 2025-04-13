from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from crud.category_crud import add_category, get_category, update_category, delete_category
from crud import category_crud

router = APIRouter()

# Thêm loại món ăn vào menu
@router.post("/categories/")
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    add_category(db=db, category=category)
    return {"message": "Category created successfully"}

@router.get("/categories")
def get_all_categories(db: Session = Depends(get_db)):
    categories = category_crud.get_all_categories(db=db)
    return {
        "message": "Categories retrieved successfully",
        "data": categories
    }