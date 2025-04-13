from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from schemas import TableCreate, TableResponse, TableUpdate
from models import Table
from fastapi import HTTPException, status
from utils.logger import get_logger

logger = get_logger(__name__)


async def create_table(db: AsyncSession, table: TableCreate):
    try:
        db_table = Table(
            name=table.name,
            is_available=table.is_available,
            table_type=table.table_type,
            capacity=table.capacity,
        )

        db.add(db_table)
        await db.commit()
        await db.refresh(db_table)
        logger.info(f"Created table: {db_table.name} (ID: {db_table.table_id})")
        
        return TableResponse.from_orm(db_table)
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error when creating table: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when creating table",
        )


async def get_table_by_id(db: AsyncSession, table_id: int):
    try:
        query = select(Table).filter(Table.table_id == table_id)
        result = await db.execute(query)
        table = result.scalars().first()
        
        if not table:
            logger.warning(f"Table not found with ID: {table_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
            )
        logger.info(f"Found table: {table.name} (ID: {table.table_id})")
        return TableResponse.from_orm(table)
    except Exception as e:
        logger.error(f"Error when finding table: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when finding table",
        )


async def get_all_tables(db: AsyncSession):
    try:
        query = select(Table)
        result = await db.execute(query)
        tables = result.scalars().all()
        logger.info(f"Found {len(tables)} tables")
        return [TableResponse.from_orm(table) for table in tables]
    except Exception as e:
        logger.error(f"Error when getting all tables: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when getting all tables",
        )


async def update_table(db: AsyncSession, table_id: int, table: TableUpdate):
    try:
        query = select(Table).filter(Table.table_id == table_id)
        result = await db.execute(query)
        db_table = result.scalars().first()
        
        if not db_table:
            logger.warning(f"Table not found with ID: {table_id} to update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
            )

        # Update information
        try:
            for field, value in table.model_dump(exclude_unset=True).items():
                setattr(db_table, field, value)
            await db.commit()
            await db.refresh(db_table)
            logger.info(f"Updated table: {db_table.name} (ID: {table_id})")
            
            return TableResponse.from_orm(db_table)
        except IntegrityError as e:
            await db.rollback()
            logger.error(f"Integrity error when updating table: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Table with this name already exists",
            )
    except Exception as e:
        logger.error(f"Unexpected error when updating table: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when updating table",
        )


async def delete_table(db: AsyncSession, table_id: int):
    try:
        query = select(Table).filter(Table.table_id == table_id)
        result = await db.execute(query)
        db_table = result.scalars().first()
        
        if not db_table:
            logger.warning(f"Table not found with ID: {table_id} to delete")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
            )

        table_name = db_table.name
        await db.delete(db_table)
        await db.commit()
        logger.info(f"Deleted table: {table_name} (ID: {table_id})")
        return TableResponse.from_orm(db_table)
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error when deleting table: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when deleting table",
        )
