from pydantic import BaseModel, Field
from typing import Optional, Annotated

class IngredientCreate(BaseModel):
    name: str
    quantity: Annotated[int, Field(ge=0)]
    unit: str
    
    class Config:
        from_attributes = True
        
class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    
    class Config:
        from_attributes = True

class IngredientResponse(BaseModel):
    ingredient_id: int
    name: str
    quantity: Annotated[int, Field(ge=0)]
    unit: str
    
    class Config:
        from_attributes = True