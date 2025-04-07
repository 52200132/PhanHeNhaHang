from pydantic import BaseModel, Field
from typing import Optional, Annotated
from enum import Enum
from datetime import datetime

class OrderStatus(str, Enum):
    not_prepared = "Chưa chuẩn bị"
    in_progress = "Đang chế biến"
    completed = "Hoàn thành"
class KitchenOrderCreate(BaseModel):
    order_id: int
    dish_id: int
    status: OrderStatus = OrderStatus.not_prepared
    note: Optional[str] = None
    quantity: Annotated[int, Field(ge=1)] = 1
    create_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
        
class KitchenOrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    note: Optional[str] = None
    quantity: Annotated[Optional[int], Field(ge=1)] = None

    class Config:
        from_attributes = True

class KitchenOrderResponse(BaseModel):
    order_id: int
    dish_id: int
    status: OrderStatus
    note: Optional[str] = None
    quantity: Annotated[int, Field(ge=1)] = 1
    create_at: datetime

    class Config:
        from_attributes = True