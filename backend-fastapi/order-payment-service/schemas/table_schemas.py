from pydantic import BaseModel
from typing import Optional, Annotated
from pydantic import Field
from pydantic import field_validator
from enum import Enum

from utils.logger import default_logger

logger = default_logger


class TableCreate(BaseModel):
    name: str
    is_available: Annotated[bool, Field(default=True)]
    table_type: Annotated[str, Field(min_length=1, max_length=255)] = "Bàn thường"
    capacity: int = Field(default=2)

    # @field_validator('table_type')
    # def validate_table_type(cls, v):
    #     if v not in ['Bàn thường', 'Bàn VIP', 'Bàn họp', 'Bàn họp VIP']:
    #         raise ValueError('Invalid table type')
    #     return v

    @field_validator("capacity")
    def validate_capacity(cls, v):
        if v < 2:
            logger.critical(f"Invalid capacity: {v}")
            raise ValueError("Invalid capacity, must be greater than 2")
        return v

class TableUpdate(BaseModel):
    name: Optional[str] = None
    is_available: Optional[bool] = None
    table_type: Optional[str] = None
    capacity: Optional[int] = None

    @field_validator("capacity")
    def validate_capacity(cls, v):
        if v is None:
            return v
        if v < 2:
            raise ValueError("Invalid capacity, must be greater than 2")
        return v


class TableResponse(BaseModel):
    table_id: int
    name: str
    is_available: bool
    table_type: str
    capacity: int

    class Config:
        # orm_mode = True
        from_attributes = True


class TableStatus(str, Enum):
    trong = "Trống"
    dang_phuc_vu = "Đang phục vụ"