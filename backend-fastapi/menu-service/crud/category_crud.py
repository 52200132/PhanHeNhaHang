from sqlalchemy.orm import Session
from models.models import Category
from schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger(__name__)

# C
# Thêm loại món ăn vào menu
def add_category(db: Session, category: CategoryCreate):
    try:
        db_category = Category(name=category.name)
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        logger.info(f"Category created: {category.name}")
        return CategoryResponse.from_orm(db_category)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating category: {str(e)}")

# R
# Lấy tất cả loại món ăn trong menu
def get_all_categories(db: Session):
    try:
        db_categories = db.query(Category).all()
        if not db_categories:
            logger.info("No categories found in database")
            raise HTTPException(status_code=404, detail="No categories found")
        logger.info(f"Retrieved {len(db_categories)} categories")
        return [CategoryResponse.from_orm(category) for category in db_categories]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving all categories: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# Lấy thông tin loại món ăn trong menu
def get_category(db: Session, category_id: int):
    try:
        db_category = db.query(Category).filter(Category.category_id == category_id).first()
        if not db_category:
            logger.warning(f"Category with ID {category_id} not found")
            raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
        logger.info(f"Retrieved category: {db_category.name} (ID: {category_id})")
        return CategoryResponse.from_orm(db_category)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# U
# Cập nhật thông tin loại món ăn trong menu
def update_category(db: Session, category_id: int, category: CategoryUpdate):
    try:
        db_category = db.query(Category).filter(Category.category_id == category_id).first()
        if not db_category:
            logger.warning(f"Category with ID {category_id} not found for update")
            raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
        
        old_name = db_category.name
        for key, value in category.dict(exclude_unset=True).items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
        logger.info(f"Category updated: {old_name} -> {db_category.name} (ID: {category_id})")
        return CategoryResponse.from_orm(db_category)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# D
# Xóa loại món ăn trong menu
def delete_category(db: Session, category_id: int):
    try:
        db_category = db.query(Category).filter(Category.category_id == category_id).first()
        if not db_category:
            logger.warning(f"Category with ID {category_id} not found for deletion")
            raise HTTPException(status_code=404, detail=f"Category with ID {category_id} not found")
        
        category_name = db_category.name
        db.delete(db_category)
        db.commit()
        logger.info(f"Category deleted: {category_name} (ID: {category_id})")
        return {"detail": "Category deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
