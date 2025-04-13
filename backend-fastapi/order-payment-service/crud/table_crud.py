from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from schemas import TableCreate, TableResponse, TableUpdate
from models import Table
from fastapi import HTTPException, status
from utils.logger import get_logger

logger = get_logger(__name__)


def create_table(db: Session, table: TableCreate):
    try:
        db_table = Table(
            name=table.name,
            is_available=table.is_available,
            table_type=table.table_type,
            capacity=table.capacity,
        )

        db.add(db_table)
        db.commit()
        db.refresh(db_table)
        logger.info(f"Created table: {db_table.name} (ID: {db_table.table_id})")
        
        return TableResponse.from_orm(db_table)
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error when creating table: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when creating table",
        )


def get_table_by_id(db: Session, table_id: int):
    try:
        table = db.query(Table).filter(Table.table_id == table_id).first()
        
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


def get_all_tables(db: Session):
    try:
        tables = db.query(Table).all()
        logger.info(f"Found {len(tables)} tables")
        return [TableResponse.from_orm(table) for table in tables]
    except Exception as e:
        logger.error(f"Error when getting all tables: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when getting all tables",
        )


def update_table(db: Session, table_id: int, table: TableUpdate):
    try:
        db_table = db.query(Table).filter(Table.table_id == table_id).first()
        
        if not db_table:
            logger.warning(f"Table not found with ID: {table_id} to update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
            )

        # Update information
        try:
            for field, value in table.model_dump(exclude_unset=True).items():
                setattr(db_table, field, value)
            db.commit()
            db.refresh(db_table)
            logger.info(f"Updated table: {db_table.name} (ID: {table_id})")
            
            return TableResponse.from_orm(db_table)
        except IntegrityError as e:
            db.rollback()
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


def delete_table(db: Session, table_id: int):
    try:
        db_table = db.query(Table).filter(Table.table_id == table_id).first()
        
        if not db_table:
            logger.warning(f"Table not found with ID: {table_id} to delete")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Table not found"
            )

        table_name = db_table.name
        db.delete(db_table)
        db.commit()
        logger.info(f"Deleted table: {table_name} (ID: {table_id})")
        return TableResponse.from_orm(db_table)
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error when deleting table: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server error when deleting table",
        )
