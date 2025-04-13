import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_STREAM_PREFIX = "order_payment_service"

# Redis stream names
ORDER_CREATED_STREAM = f"{REDIS_STREAM_PREFIX}:order_created"
ORDER_DETAIL_DELETED_STREAM = f"{REDIS_STREAM_PREFIX}:order_detail_deleted"

ORDER_UPDATED_STREAM = f"{REDIS_STREAM_PREFIX}:order_updated"
ORDER_STATUS_CHANGED_STREAM = f"{REDIS_STREAM_PREFIX}:order_status_changed"
PAYMENT_PROCESSED_STREAM = f"{REDIS_STREAM_PREFIX}:payment_processed"
TABLE_STATUS_STREAM = f"{REDIS_STREAM_PREFIX}:table_status"