from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.sesstion import get_db
from schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from crud.category_crud import add_category, get_category_by_id, update_category, delete_category, get_categories


router = APIRouter()

@router.post("/categories/")
async def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    add_category(db=db, category=category)
    return {"message": "Category created successfully"}

@router.get("/categories/{category_id}")
async def read_category(category_id: int, db: Session = Depends(get_db)):
    return {
        "category_item": get_category_by_id(db=db, category_id=category_id)
    }

@router.get("/categories/")
async def get_all_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # print("\033[35m")
    # print("Get all categories - category_routes.py")
    # print('\033[0m')
    result = get_categories(db=db, skip=skip, limit=limit)
    # print(result)
    return {
        "category_items": result
    }
