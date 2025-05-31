from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db

from schemas.table_schemas import TableStatus
from schemas import TableCreate, TableUpdate, TableResponse, ServiceResponseModel
from crud import table_crud
from utils.logger import default_logger

router = APIRouter(prefix="/tables", tags=["tables"])

logger = default_logger

@router.post("/", response_model=ServiceResponseModel)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    try:
        created_table = table_crud.create_table(db, table)
        return ServiceResponseModel(
            message="Create table successfully",
            success=True,
            data=created_table
        )
    except Exception as e:
        logger.error(f"Error when creating table: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when creating table"
        )

@router.get("/{table_id}", response_model=ServiceResponseModel)
def get_table(table_id: int, db: Session = Depends(get_db)):
    try:
        table = table_crud.get_table_by_id(db, table_id)
        return ServiceResponseModel(
            message="Get table successfully",
            success=True,
            data=table
        )
    except Exception as e:
        logger.error(f"Error when getting table information: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when getting table information"
        )

@router.get("/")
def get_all_tables(db: Session = Depends(get_db)):
    try:
        tables = table_crud.get_all_tables(db)
        return {
            "message": "Get all tables successfully",
            "success": True,
            "data": tables
        }
    except Exception as e:
        logger.error(f"Error when getting all tables: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when getting all tables"
        )

@router.put("/{table_id}", response_model=ServiceResponseModel)
def update_table(table_id: int, table: TableUpdate, db: Session = Depends(get_db)):
    try:
        updated_table = table_crud.update_table(db, table_id, table)
        return ServiceResponseModel(
            message="Update table successfully",
            success=True,
            data=updated_table
        )
    except Exception as e:
        logger.error(f"Error when updating table: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when updating table"
        )

@router.delete("/{table_id}", response_model=ServiceResponseModel)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    try:
        result = table_crud.delete_table(db, table_id)
        return ServiceResponseModel(
            message="Delete table successfully",
            success=True,
            data=result
        )
    except Exception as e:
        logger.error(f"Error when deleting table: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when deleting table"
        )

@router.patch("/{table_id}/update-status")
def patch_table(table_id: int, status: TableStatus, db: Session = Depends(get_db)):
    try:
        is_available = False
        if status == TableStatus.dang_phuc_vu:
            is_available = False
        elif status == TableStatus.trong:
            is_available = True
        table_update = TableUpdate(is_available=is_available)
        updated_table = table_crud.update_table(db, table_id, table_update)
        return {
            "message": "Update table status successfully",
            "success": True,
            "data": updated_table
        }
    except Exception as e:
        logger.error(f"Error when updating table status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error when updating table status"
        )