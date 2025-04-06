from sqlalchemy import Column, Integer, Unicode, Enum, ForeignKey, Boolean, DateTime, Text, CheckConstraint
from sqlalchemy.orm import relationship
from db import Base  

class Dish(Base):
    __tablename__ = "Dish"

    dish_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    category_id = Column(Integer, ForeignKey("Category.category_id"), nullable=False)
    name = Column(Unicode(255), nullable=False)
    price = Column(Integer, nullable=False)
    unit_price = Column(Unicode(50), nullable=False, default="VNĐ") # đơn vị tiền tệ
    img_path = Column(Unicode(255), nullable=True)
    description = Column(Unicode(255), nullable=True)
    is_available = Column(Boolean, default=False)

    category = relationship("Category", back_populates="dishes") # checked
    # order_details = relationship("OrderDetail", back_populates="Dish")
    recipes  = relationship("Recipe", back_populates="dish") # checked

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_positive")
    )


class Category(Base):
    __tablename__ = "Category"

    category_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(Unicode(255), nullable=False)

    dishes = relationship("Dish", back_populates="category") #checked

class Ingredient(Base):
    __tablename__ = "Ingredient"

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(Unicode(255), nullable=False)
    unit = Column(Unicode(50), nullable=False)
    quantity = Column(Integer, nullable=False)

    recipes = relationship("Recipe", back_populates="ingredient") # checked

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_positive")
    )


class Recipe(Base):
    __tablename__ = "Recipe"

    recipe_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    dish_id = Column(Integer, ForeignKey("Dish.dish_id"))
    ingredient_id = Column(Integer, ForeignKey("Ingredient.ingredient_id"))
    is_main = Column(Boolean, default=False)
    unit = Column(Unicode(50), nullable=False)
    base_amount = Column(Integer, nullable=False)

    dish = relationship("Dish", back_populates="recipes") # checked
    ingredient = relationship("Ingredient", back_populates="recipes") # checked