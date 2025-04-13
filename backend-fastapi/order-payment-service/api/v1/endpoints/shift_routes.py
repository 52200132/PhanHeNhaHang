from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from schemas import ShiftCreate, ShiftUpdate, ShiftResponse, ServiceResponseModel
from crud import shift_crud
from utils.logger import default_logger

router = APIRouter(prefix="/shifts", tags=["shifts"])

logger = default_logger

@router.post("/", response_model=ServiceResponseModel)
def create_shift(shift: ShiftCreate, db: Session = Depends(get_db)):
    try:
        created_shift = shift_crud.create_shift(db, shift)
        return ServiceResponseModel(
            message="Create shift successfully",
            success=True,
            data=created_shift
        )
    except Exception as e:
        logger.error(f"Error when creating shift: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when creating shift"
        )

@router.get("/{shift_id}", response_model=ServiceResponseModel)
def get_shift(shift_id: int, db: Session = Depends(get_db)):
    try:
        shift = shift_crud.get_shift_by_id(db, shift_id)
        return ServiceResponseModel(
            message="Get shift successfully",
            success=True,
            data=shift
        )
    except Exception as e:
        logger.error(f"Error when getting shift information: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when getting shift information"
        )

@router.get("/", response_model=ServiceResponseModel)
def get_all_shifts(db: Session = Depends(get_db)):
    try:
        shifts = shift_crud.get_all_shifts(db)
        return ServiceResponseModel(
            message="Get all shifts successfully",
            success=True,
            data=shifts
        )
    except Exception as e:
        logger.error(f"Error when getting all shifts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when getting all shifts"
        )

@router.put("/{shift_id}", response_model=ServiceResponseModel)
def update_shift(shift_id: int, shift: ShiftUpdate, db: Session = Depends(get_db)):
    try:
        updated_shift = shift_crud.update_shift(db, shift_id, shift)
        return ServiceResponseModel(
            message="Update shift successfully",
            success=True,
            data=updated_shift
        )
    except Exception as e:
        logger.error(f"Error when updating shift: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when updating shift"
        )

@router.delete("/{shift_id}", response_model=ServiceResponseModel)
def delete_shift(shift_id: int, db: Session = Depends(get_db)):
    try:
        result = shift_crud.delete_shift(db, shift_id)
        return ServiceResponseModel(
            message="Delete shift successfully",
            success=True,
            data=result
        )
    except Exception as e:
        logger.error(f"Error when deleting shift: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when deleting shift"
        )