from db import Base
from sqlalchemy import Column, Unicode, Integer, ForeignKey, DateTime, Enum, Boolean, CheckConstraint, Time
from sqlalchemy.orm import relationship 

class Table(Base):
    __tablename__ = "Table"

    table_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(Unicode(255), nullable=False)
    is_available = Column(Boolean, default=True)
    table_type = Column(Unicode(255), nullable=False)
    capacity = Column(Integer, nullable=False)

    orders = relationship("Order", back_populates="table") # checked

    __table_args__ = (
        CheckConstraint("capacity >= 2", name="check_capacity_greater_than_2"),
    )

class Order(Base):
    __tablename__ = "Order"

    order_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    table_id = Column(Integer, ForeignKey("Table.table_id"), nullable=False)
    # user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total_price = Column(Integer, nullable=False, default=0)
    unit_price = Column(Unicode(50), nullable=False, default="VNĐ") # đơn vị tiền tệ
    checkIn_time = Column(DateTime, nullable=False)
    checkOut_time = Column(DateTime, nullable=False)
    status = Column(Enum("Chờ xử lý", "Chờ xác nhận", "Hủy", "Đang chế biến", "Hoàn thành"), nullable=False, default="Chờ xử lý")
    is_paid = Column(Boolean, default=False)

    table = relationship("Table", back_populates="orders") # checked
    # user = relationship("User", back_populates="orders")
    payment = relationship("Payment", back_populates="order") # checked
    order_details = relationship("OrderDetail", back_populates="order") # checked
    
    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_positive"),  # Thêm dấu phẩy ở đây
    )

class OrderDetail(Base):
    __tablename__ = "OrderDetail"

    orderDetail_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    order_id = Column(Integer, ForeignKey("Order.order_id"), nullable=False)
    # dish_id = Column(Integer, ForeignKey("dishes.dish_id"), nullable=False)
    dish_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Unicode(50), nullable=False)
    total_price = Column(Integer, nullable=False, default=0)
    note = Column(Unicode(255), nullable=True)

    order = relationship("Order", back_populates="order_details") # checked
    # dish = relationship("Dish", back_populates="order_details")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_positive"),
        CheckConstraint("total_price >= 0", name="check_total_price_positive"),
    )

class Shift(Base):
    __tablename__ = "Shift"

    shift_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(Unicode(255), nullable=False)
    shift_start = Column(Time, nullable=False)
    shift_end = Column(Time, nullable=False)

    payments = relationship("Payment", back_populates="shift") # checked

class Payment(Base):
    __tablename__ = "Payment"

    payment_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    order_id = Column(Integer, ForeignKey("Order.order_id"), nullable=False)
    shift_id = Column(Integer, ForeignKey("Shift.shift_id"), nullable=False)
    payment_amount = Column(Integer, nullable=False)
    unit_price = Column(Unicode(50), nullable=False, default="VNĐ") # đơn vị tiền tệ
    payment_method = Column(Unicode(50), nullable=False)
    payment_time = Column(DateTime, nullable=False)
    transaction_id = Column(Unicode(255), nullable=False) # mã giao dịch

    shift = relationship("Shift", back_populates="payments") # checked
    order = relationship("Order", back_populates="payment") # checked

    __table_args__ = (
        CheckConstraint("payment_amount >= 0", name="check_payment_amount_positive"),
    )