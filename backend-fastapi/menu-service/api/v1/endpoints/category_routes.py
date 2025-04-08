from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.sesstion import get_db
from schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from crud.category_crud import add_category, get_category, update_category, delete_category, get_all_categories


router = APIRouter()

# Thêm loại món ăn vào menu
@router.post("/categories/")
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = add_category(db=db, category=category)
    return new_category

# Lấy tất cả loại món ăn trong menu
@router.get("/categories/", response_model=list[CategoryResponse])
def read_all_categories(db: Session = Depends(get_db)):
    categories = get_all_categories(db=db)
    return categories
# Lấy loại món ăn trong menu theo id
@router.get("/categories/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db=db, category_id=category_id)
    return category

# Cập nhật thông tin loại món ăn trong menu
@router.patch("/categories/{category_id}")
def update_existing_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    updated_category = update_category(db=db, category_id=category_id, category=category)
    return updated_category

# Xóa loại món ăn trong menu
@router.delete("/categories/{category_id}")
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    deleted_category = delete_category(db=db, category_id=category_id)
    return deleted_category
