import redis.asyncio as redis
import pickle
from redis.exceptions import RedisError  # Sử dụng RedisError từ redis.exceptions
from utils.logger import get_logger

logger = get_logger(__name__)

class RedisStreamConsumer:
    """
    Redis Stream Consumer để tiêu thụ các thông điệp từ Redis Streams.
    """
    def __init__(self, host: str, port: int, streams: dict, group_name: str, consumer_name: str, message_handler):
        self.redis_client = None
        self.host = host
        self.port = port
        self.streams = streams
        self.group_name = group_name
        self.consumer_name = consumer_name
        self.message_handler = message_handler

    async def connect(self):
        """
        Initialize the Redis connection
        """
        try:
            self.redis_client = redis.Redis(
                host=self.host,
                port=self.port,
                decode_responses=False
            )
            await self.redis_client.ping()
            # Create consumer groups if they don't exist
            for stream in self.streams.keys():
                try:
                    await self.redis_client.xgroup_create(stream, self.group_name, id="0", mkstream=True)
                except RedisError as e:
                    if "BUSYGROUP" in str(e):
                        logger.info(f"Consumer group {self.group_name} already exists for stream {stream}")
                    else:
                        raise e
            logger.info("Redis Stream Consumer connected")
        except RedisError as e:
            logger.error(f"Error connecting to Redis: {str(e)}")
            raise

    async def consume(self):
        """
        Consume messages từ Redis Streams
        """
        try:
            while True:
                messages = await self.redis_client.xreadgroup(
                    groupname=self.group_name,
                    consumername=self.consumer_name,
                    streams=self.streams,
                    count=10,
                    block=5000
                )
                for stream, entries in messages:
                    for entry_id, data in entries:
                        try:
                            # Giải mã dữ liệu
                            deserialized_data = {key.decode("utf-8"): pickle.loads(value) for key, value in data.items()}
                            deserialized_data = deserialized_data.get("data")
                            logger.info(f"Message received from stream {stream}: {deserialized_data}")
                            await self.message_handler(stream.decode("utf-8"), deserialized_data)
                            await self.redis_client.xack(stream.decode("utf-8"), self.group_name, entry_id)
                        except Exception as e:
                            logger.error(f"Error processing message: {str(e)}")
        except RedisError as e:
            logger.error(f"Redis Stream Consumer error: {str(e)}")

    async def stop(self):
        """
        Stop the consumer
        """
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Redis Stream Consumer stopped")
