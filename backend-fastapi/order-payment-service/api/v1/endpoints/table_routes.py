from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from schemas import TableCreate, TableUpdate, TableResponse, ServiceResponseModel
from crud import table_crud
from utils.logger import default_logger

router = APIRouter(prefix="/tables", tags=["tables"])

logger = default_logger

@router.post("/", response_model=ServiceResponseModel)
async def create_table(table: TableCreate, db: AsyncSession = Depends(get_db)):
    try:
        created_table = await table_crud.create_table(db, table)
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
async def get_table(table_id: int, db: AsyncSession = Depends(get_db)):
    try:
        table = await table_crud.get_table_by_id(db, table_id)
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
async def get_all_tables(db: AsyncSession = Depends(get_db)):
    try:
        tables = await table_crud.get_all_tables(db)
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
async def update_table(table_id: int, table: TableUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_table = await table_crud.update_table(db, table_id, table)
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
async def delete_table(table_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await table_crud.delete_table(db, table_id)
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
