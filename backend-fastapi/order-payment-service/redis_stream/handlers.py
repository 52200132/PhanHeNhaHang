import asyncio
from fastapi import Depends

from utils.logger import get_logger
from crud import order_crud
from db.session import get_db
from schemas.order_schemas import OrderResonpense

logger = get_logger(__name__)


async def handle_order_created(data: dict):
    """Handle order created event"""
    # order = OrderResonpense.parse_obj(data.get("data"))
    # logger.info(f"Processing order created event: {order.checkIn_time}")


async def handle_order_updated(data):
    """Handle order updated event"""
    logger.info(f"Processing order updated event: {data}")


async def handle_orderdetail_from_order_deleted(data):
    """Xử lý sự món ăn trong đơn hàng bị xóa"""
    logger.info(f"Processing order detail deleted event: {data}")
    order_detail_id = data.get("order_detail_id")
    print(f"order_detail_id: {order_detail_id}")
    if not order_detail_id:
        logger.error("order_detail_id not found in data")
        return
    logger.info(f"Processing order detail deleted event: {order_detail_id}")
    await order_crud.delete_dish_from_order(Depends(get_db), order_detail_id)


async def handle_order_status_changed(data):
    """Handle order status changed event"""
    logger.info(f"Processing order status changed event: {data}")


async def handle_payment_processed(data):
    """Handle payment processed event"""
    logger.info(f"Processing payment processed event: {data}")


async def handle_table_status(data):
    """Handle table status event"""
    logger.info(f"Processing table status event: {data}")


async def handle_redis_message(stream, data):
    """Unified handler for Redis Stream messages"""
    logger.info(f"Handle message from '{stream}'")
    if "order_created" in stream:
        await handle_order_created(data)  # Sử dụng await
    elif "order_updated" in stream:
        await handle_order_updated(data)  # Sử dụng await
    elif "order_detail_deleted" in stream:
        await handle_orderdetail_from_order_deleted(data)  # Sử dụng await
    elif "order_status_changed" in stream:
        await handle_order_status_changed(data)  # Sử dụng await
    elif "payment_processed" in stream:
        await handle_payment_processed(data)  # Sử dụng await
    elif "table_status" in stream:
        await handle_table_status(data)  # Sử dụng await
    else:
        logger.warning(f"No handler for stream: {stream}")
