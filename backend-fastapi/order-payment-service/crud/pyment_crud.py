from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import uuid4

from crud import shift_crud
from models.models import Payment
from schemas.payment_schemas import PaymentShow
from utils.logger import get_logger


logger = get_logger(__name__)

async def create_payment(db: AsyncSession, payment: PaymentShow):
    try:
        payment_time = payment.payment_time.time()
        shift_id = (await shift_crud.get_shift_by_time(db, payment_time = payment.payment_time.time())).shift_id

        db_payment = Payment(
            order_id=payment.order_id,
            shift_id=shift_id,
            payment_amount=payment.payment_amount,
            unit_price="VNĐ",
            payment_method=payment.payment_method,
            payment_time=payment_time,
            transaction_id=uuid4().hex  # Generate a unique transaction ID
        )
        
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)
        
        return PaymentSchema.from_orm(db_payment)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating payment: {str(e)}"
        )