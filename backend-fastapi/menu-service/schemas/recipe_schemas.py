from pydantic import BaseModel, Field
from typing import Optional, Annotated

class RecipeCreate(BaseModel):
    ingredient_id: int
    dish_id: int
    unit: str
    base_amount: Annotated[int, Field(gt=0)]

    class Config:
        from_attributes = True

class RecipeUpdate(BaseModel):
    ingredient_id: Optional[int] = None
    dish_id: Optional[int] = None
    unit: Optional[str] = None
    base_amount: Optional[int] = None

    class Config:
        from_attributes = True

class RecipeResponse(BaseModel):
    recipe_id: int
    ingredient_id: int
    dish_id: int
    unit: str
    base_amount: Annotated[int, Field(gt=0)]

    class Config:
        from_attributes = True