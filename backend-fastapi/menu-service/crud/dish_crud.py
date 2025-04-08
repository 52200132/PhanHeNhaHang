from sqlalchemy.orm import Session
from models.models import Dish
from schemas.dish_schemas import DishCreate, DishUpdate, DishResponse
from fastapi import HTTPException

#C
def add_dish(db: Session, dish: DishCreate):
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
    return DishResponse.from_orm(db_dish)
#R
def get_dish(db: Session, dish_id: int):
    db_dish = db.query(Dish).filter(Dish.dish_id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail=f"Dish with ID {dish_id} not found")
    return DishResponse.from_orm(db_dish)

#get all dishes
def get_all_dish(db: Session):
    db_dish = db.query(Dish).all()
    if not db_dish:
        raise HTTPException(status_code=404, detail="No dishes found")
    return [DishResponse.from_orm(dish) for dish in db_dish]

#get all dishes by category
def get_all_dish_by_category(db: Session, category_id: int):
    db_dish = db.query(Dish).filter(Dish.category_id == category_id).all()
    if not db_dish:
        raise HTTPException(status_code=404, detail=f"No dishes found for category ID {category_id}")
    return [DishResponse.from_orm(dish) for dish in db_dish]


#U
def update_dish(db: Session, dish_id: int, dish: DishUpdate):
    db_dish = db.query(Dish).filter(Dish.dish_id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail=f"Dish with ID {dish_id} not found")
    for key, value in dish.dict(exclude_unset=True).items():
        setattr(db_dish, key, value)
    db.commit()
    db.refresh(db_dish)
    return DishResponse.from_orm(db_dish)

#D
def delete_dish(db: Session, dish_id: int):
    db_dish = db.query(Dish).filter(Dish.dish_id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail=f"Dish with ID {dish_id} not found")
    db.delete(db_dish)
    db.commit()
    return {"detail": "Dish deleted successfully"}