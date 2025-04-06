from sqlalchemy.orm import Session

def add_dish(db: Session, dish):
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish