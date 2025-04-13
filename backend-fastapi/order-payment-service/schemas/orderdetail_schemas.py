from pydantic import BaseModel
from typing import Optional

class OrderDetailSchema(BaseModel):
    orderDetail_id: Optional[int]
    order_id: int
    dish_id: int
    quantity: int = 1
    unit_price: str
    total_price: int
    note: Optional[str]

    class Config:
        orm_mode = True 


class OrderDetailCreate(BaseModel):
    """
    order_id: Optional[int] = None\n
    dish_id: int\n
    quantity: int = 1\n
    total_price: Optional[int] = None\n
    note: Optional[str] = ""\n
    """
    order_id: Optional[int] = None
    dish_id: int
    quantity: int = 1
    total_price: Optional[int] = None
    note: Optional[str] = ""

class OrderDetail(BaseModel):
    dish_id: int
    quantity: int = 1
    note: Optional[str] = ""


# Order detail response schema
class OrderDetailResponse(BaseModel):
    orderDetail_id: int
    order_id: int
    dish_id: int
    quantity: int
    total_price: int
    unit_price: str = "VNĐ"
    note: str = ""
    is_deleted: bool = False

    class Config:
        from_attributes = True