from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from datetime import time

from models import Shift
from schemas import ShiftCreate, ShiftUpdate, ShiftResponse
from utils.logger import default_logger

logger = default_logger

async def create_shift(db: AsyncSession, shift: ShiftCreate):
    try:
        # Validate shift times
        if shift.shift_end <= shift.shift_start:
            logger.error(f"Invalid shift times: end ({shift.shift_end}) <= start ({shift.shift_start})")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shift end time must be after start time"
            )

        db_shift = Shift(
            name=shift.name,
            shift_start=shift.shift_start,
            shift_end=shift.shift_end
        )
        
        try:
            db.add(db_shift)
            await db.commit()
            await db.refresh(db_shift)
            logger.info(f"Created shift: {db_shift.name} (ID: {db_shift.shift_id})")
            return ShiftResponse.from_orm(db_shift)
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Integrity error when creating shift: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shift with this name already exists"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error when creating shift: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when creating shift"
        )

async def get_shift_by_id(db: AsyncSession, shift_id: int):
    try:
        query = select(Shift).filter(Shift.shift_id == shift_id)
        result = await db.execute(query)
        shift = result.scalars().first()
        
        if not shift:
            logger.warning(f"Shift not found with ID: {shift_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shift not found"
            )
        logger.info(f"Found shift: {shift.name} (ID: {shift.shift_id})")
        return ShiftResponse.from_orm(shift)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error when finding shift: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when getting shift"
        )

async def get_shift_by_time(db: AsyncSession, time: time):
    try:
        query = select(Shift).filter(
            time > Shift.shift_start,
            time <= Shift.shift_end
        )
        result = await db.execute(query)
        shift = result.scalars().first()
        
        if not shift:
            logger.warning(f"No shift found for time: {time}")
            query = select(Shift).order_by(Shift.shift_id.asc())
            result = await db.execute(query)
            shift = result.scalars().first()
        logger.info(f"Found shift: {shift.name} for time: {time}")
        return ShiftResponse.from_orm(shift)
    except IntegrityError as e:
        logger.error(f"Integrity error when finding shift: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shift with this name already exists"
        )
    except Exception as e:
        logger.error(f"Unexpected error when finding shift: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when getting shift"
        )

async def get_all_shifts(db: AsyncSession):
    try:
        query = select(Shift)
        result = await db.execute(query)
        shifts = result.scalars().all()
        
        logger.info(f"Retrieved {len(shifts)} shifts")
        return [ShiftResponse.from_orm(shift) for shift in shifts]
    except Exception as e:
        logger.error(f"Error when getting all shifts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when getting all shifts"
        )

async def update_shift(db: AsyncSession, shift_id: int, shift: ShiftUpdate):
    try:
        query = select(Shift).filter(Shift.shift_id == shift_id)
        result = await db.execute(query)
        db_shift = result.scalars().first()
        
        if not db_shift:
            logger.warning(f"Shift not found with ID: {shift_id} to update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shift not found"
            )

        # Fields to update
        update_data = shift.model_dump(exclude_unset=True)
        
        # Validate time fields
        if 'shift_start' in update_data and 'shift_end' in update_data:
            if update_data['shift_end'] <= update_data['shift_start']:
                logger.error(f"Invalid shift times in update: end ({update_data['shift_end']}) <= start ({update_data['shift_start']})")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Shift end time must be after start time"
                )
        elif 'shift_start' in update_data: # If only start time is updated
            shift_end = db_shift.shift_end
            if update_data['shift_start'] >= shift_end:
                logger.error(f"Invalid shift times in update: start ({update_data['shift_start']}) >= end ({shift_end})")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Shift start time must be before end time"
                )
        elif 'shift_end' in update_data: # If only end time is updated
            shift_start = db_shift.shift_start
            if update_data['shift_end'] <= shift_start:
                logger.error(f"Invalid shift times in update: end ({update_data['shift_end']}) <= start ({shift_start})")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Shift end time must be after start time"
                )

        try:
            for field, value in update_data.items():
                setattr(db_shift, field, value)
            await db.commit()
            await db.refresh(db_shift)
            logger.info(f"Updated shift: {db_shift.name} (ID: {shift_id})")
            return ShiftResponse.from_orm(db_shift)
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Integrity error when updating shift: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shift with this name already exists"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error when updating shift: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when updating shift"
        )

async def delete_shift(db: AsyncSession, shift_id: int):
    try:
        query = select(Shift).filter(Shift.shift_id == shift_id)
        result = await db.execute(query)
        db_shift = result.scalars().first()
        
        if not db_shift:
            logger.warning(f"Shift not found with ID: {shift_id} to delete")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shift not found"
            )
        
        shift_name = db_shift.name
        await db.delete(db_shift)
        await db.commit()
        logger.info(f"Deleted shift: {shift_name} (ID: {shift_id})")
        return {"message": "Shift deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error when deleting shift: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when deleting shift"
        )