from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentSchema(BaseModel):
    payment_id: Optional[int]
    order_id: int
    shift_id: int
    payment_amount: int
    unit_price: str = "VNĐ"
    payment_method: str
    payment_time: datetime
    transaction_id: str

    class Config:
        from_attributes = True

class PaymentShow(BaseModel):
    order_id: int
    payment_amount: int
    payment_method: str
    payment_time: datetime

class PaymentResponse(BaseModel):
    payment_id: int
    order_id: int
    shift_id: int
    payment_amount: int
    unit_price: str = "VNĐ"
    payment_method: str
    payment_time: datetime
    transaction_id: str

    class Config:
        from_attributes = True