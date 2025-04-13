from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

from schemas.orderdetail_schemas import OrderDetailCreate

class OrderStatus(str, Enum):
    cho_xu_ly = "Chờ xử lý"
    cho_xac_nhan = "Chờ xác nhận"
    huy = "Hủy"
    dang_che_bien = "Đang chế biến"
    hoan_thanh = "Hoàn thành"

class MakeOrder(BaseModel):
    table_id: int
    items: list[OrderDetailCreate]


class OrderResonpense(BaseModel):
    order_id: int
    table_id: int
    total_price: int
    unit_price: str
    checkIn_time: datetime
    checkOut_time: datetime
    status: OrderStatus
    is_paid: bool

    class Config:
        from_attributes = True
