from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    
    class Config:
        from_attributes = True
class CategoryUpdate(BaseModel):
    name: str

    class Config:
        from_attributes = True
        
class CategoryResponse(BaseModel):
    category_id: int
    name: str

    class Config:
        from_attributes = True