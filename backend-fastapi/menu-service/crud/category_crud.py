from sqlalchemy.orm import Session
from models.models import Category
from schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from fastapi import HTTPException

# C
# Thêm loại món ăn vào menu
def add_category(db: Session, category: CategoryCreate):
    db_category = Category(
       name=category.name
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return CategoryResponse.from_orm(db_category)

# R
# Lấy tất cả loại món ăn trong menu
def get_all_categories(db: Session):
    db_categories = db.query(Category).all()
    if not db_categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return {
        "message": "Categories retrieved successfully",
        "data": [CategoryResponse.from_orm(category) for category in db_categories]
    }
# Lấy thông tin loại món ăn trong menu
def get_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
    return CategoryResponse.from_orm(db_category)

# U
# Cập nhật thông tin loại món ăn trong menu
def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return CategoryResponse.from_orm(db_category)

# D
# Xóa loại món ăn trong menu
def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
    db.delete(db_category)
    db.commit()
    return {"detail": "Category deleted successfully"}
