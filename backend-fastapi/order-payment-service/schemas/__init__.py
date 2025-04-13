from .table_schemas import TableCreate, TableResponse, TableUpdate
from .order_schemas import OrderResonpense, MakeOrder
from .orderdetail_schemas import OrderDetailSchema
from .shift_schemas import ShiftCreate, ShiftUpdate, ShiftResponse
from .payment_schemas import PaymentSchema
from pydantic import BaseModel
from typing import Optional

class ServiceResponseModel(BaseModel):
    message: str
    success: bool
    data: Optional[object] = None

__all__ = [
    "TableCreate",
    "TableResponse",
    "TableUpdate",
    "OrderResonpense",
    "MakeOrder",
    "ShiftCreate",
    "ShiftUpdate",
    "ShiftResponse",
    "PaymentSchema",
    "ServiceResponseModel",
]