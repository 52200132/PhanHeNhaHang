from db import Base
from sqlalchemy import Column, Integer, DateTime, Unicode, Enum, CheckConstraint

class KitchenOrder(Base):
    __tablename__ = "KitchenOrder"

    kitchen_order_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    order_id = Column(Integer, nullable=False)
    dish_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    note = Column(Unicode(255), nullable=True)
    create_at = Column(DateTime, nullable=False)
    status = Column(Enum("Chưa chuẩn bị", "Đang chế biến", "Hoàn thành"), nullable=False, default="Chưa chuẩn bị")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
    )