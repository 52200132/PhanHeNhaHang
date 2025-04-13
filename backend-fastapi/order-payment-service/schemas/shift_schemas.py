from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import time


class ShiftBase(BaseModel):
    name: str = Field(..., description="Name of the shift")
    shift_start: time = Field(..., description="Start time of the shift")
    shift_end: time = Field(..., description="End time of the shift")

    @validator("shift_end")
    def validate_shift_time(cls, v, values):
        shift_start = values.get("shift_start")
        if not shift_start:
            raise ValueError("shift_start is required")
        if v <= shift_start:
            raise ValueError("shift_end must be greater than shift_start")
        return v


class ShiftCreate(ShiftBase):
    pass


class ShiftUpdate(BaseModel):
    name: Optional[str] = None
    shift_start: Optional[time] = None
    shift_end: Optional[time] = None


class ShiftResponse(BaseModel):
    shift_id: int
    name: str
    shift_start: time
    shift_end: time

    class Config:
        from_attributes = True
