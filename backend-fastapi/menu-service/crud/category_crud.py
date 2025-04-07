from sqlalchemy.orm import Session
from models.models import Category
from schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from fastapi import HTTPException


def add_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return CategoryResponse.from_orm(db_category)


def get_category_by_id(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryResponse.from_orm(db_category)


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    # print("\033[35m")
    # print("Get all categories - category_crud.py")
    # print('\033[0m')
    category_items = db.query(Category).order_by(Category.category_id).offset(skip).limit(limit).all()
    # print(category_items)
    return [CategoryResponse.from_orm(category) for category in category_items]


def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return CategoryResponse.from_orm(db_category)


def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.category_id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"detail": "Category deleted successfully"}
