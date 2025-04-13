from sqlalchemy.orm import Session
from models.models import Dish
from schemas.dish_schemas import DishCreate, DishUpdate, DishResponse
from fastapi import HTTPException
from utils.logger import get_logger

logger = get_logger(__name__)

#C
def add_dish(db: Session, dish: DishCreate):
    try:
        db_dish = Dish(
            name=dish.name,
            price=dish.price,
            unit_price=dish.unit_price,
            img_path=dish.img_path,
            description=dish.description,
            is_available=dish.is_available,
            category_id=dish.category_id
        )
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
        logger.info(f"Dish created: {dish.name} (Price: {dish.price})")
        return DishResponse.from_orm(db_dish)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating dish: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating dish: {str(e)}")

#R
def get_dish(db: Session, dish_id: int):
    try:
        db_dish = db.query(Dish).filter(Dish.dish_id == dish_id).first()
        if not db_dish:
            logger.warning(f"Dish with ID {dish_id} not found")
            raise HTTPException(status_code=404, detail=f"Dish with ID {dish_id} not found")
        logger.info(f"Retrieved dish: {db_dish.name} (ID: {dish_id})")
        return DishResponse.from_orm(db_dish)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving dish {dish_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

#get all dishes
def get_all_dish(db: Session):
    try:
        db_dish = db.query(Dish).all()
        if not db_dish:
            logger.info("No dishes found in database")
            raise HTTPException(status_code=404, detail="No dishes found")
        logger.info(f"Retrieved {len(db_dish)} dishes")
        return {
            "message": "Dishes retrieved successfully",
            "data": [DishResponse.from_orm(dish) for dish in db_dish]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving all dishes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

#get all dishes by category
def get_all_dish_by_category(db: Session, category_id: int):
    try:
        db_dish = db.query(Dish).filter(Dish.category_id == category_id).all()
        if not db_dish:
            logger.warning(f"No dishes found for category ID {category_id}")
            raise HTTPException(status_code=404, detail=f"No dishes found for category ID {category_id}")
        logger.info(f"Retrieved {len(db_dish)} dishes for category ID {category_id}")
        return {
            "message": "Dishes retrieved successfully",
            "data": [DishResponse.from_orm(dish) for dish in db_dish]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving dishes for category {category_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

#U
def update_dish(db: Session, dish_id: int, dish: DishUpdate):
    try:
        db_dish = db.query(Dish).filter(Dish.dish_id == dish_id).first()
        if not db_dish:
            logger.warning(f"Dish with ID {dish_id} not found for update")
            raise HTTPException(status_code=404, detail=f"Dish with ID {dish_id} not found")
        
        update_data = dish.dict(exclude_unset=True)
        logger.info(f"Updating dish {dish_id} with data: {update_data}")
        
        for key, value in update_data.items():
            setattr(db_dish, key, value)
        db.commit()
        db.refresh(db_dish)
        logger.info(f"Dish updated successfully: {db_dish.name} (ID: {dish_id})")
        return DishResponse.from_orm(db_dish)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating dish {dish_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

#D
def delete_dish(db: Session, dish_id: int):
    try:
        db_dish = db.query(Dish).filter(Dish.dish_id == dish_id).first()
        if not db_dish:
            logger.warning(f"Dish with ID {dish_id} not found for deletion")
            raise HTTPException(status_code=404, detail=f"Dish with ID {dish_id} not found")
        
        dish_name = db_dish.name
        db.delete(db_dish)
        db.commit()
        logger.info(f"Dish deleted successfully: {dish_name} (ID: {dish_id})")
        return {"detail": "Dish deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting dish {dish_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")