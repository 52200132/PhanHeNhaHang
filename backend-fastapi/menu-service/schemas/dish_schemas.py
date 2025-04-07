from pydantic import BaseModel, Field
from typing import Optional, Annotated

class DishCreate(BaseModel):
    name: str
    price: Annotated[int, Field(gt=0)]
    unit_price: str
    img_path: Optional[str] = None
    description: Optional[str] = None
    is_available: bool = True
    category_id: int

    class Config:
        from_attributes = True

class DishUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    unit_price: Optional[str] = None
    img_path: Optional[str] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None
    category_id: Optional[int] = None

    class Config:
        from_attributes = True

class DishResponse(BaseModel):
    dish_id: int
    name: str
    price: Annotated[int, Field(gt=0)]
    unit_price: str
    img_path: Optional[str] = None
    description: Optional[str] = None
    is_available: bool
    category_id: int

    class Config:
        from_attributes = True