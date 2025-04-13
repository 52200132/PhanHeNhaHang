import redis.asyncio as redis
import pickle
from utils.logger import get_logger

logger = get_logger(__name__)

class RedisStreamProducer:
    """
    Redis Stream Producer to send messages to Redis Streams
    """
    def __init__(self, host: str, port: int):
        self.redis_client = None
        self.host = host
        self.port = port

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
            # Test the connection
            await self.redis_client.ping()
            logger.info("Redis Stream Producer connected")
        except Exception as e:
            logger.error(f"Error connecting to Redis: {str(e)}")
            raise

    async def produce_message(self, stream: str, data):
        """
        Send a message to a Redis Stream

        Args:
            stream (str): Redis Stream name
            data (dict): Message data
        """
        try:
            serialized_data = pickle.dumps(data)
            await self.redis_client.xadd(stream, {"data": serialized_data})
            logger.info(f"Message sent to stream {stream}: {data}")
        except Exception as e:
            logger.error(f"Error sending message to Redis Stream: {str(e)}")

# Create a singleton instance of the producer
redis_producer = RedisStreamProducer(host="localhost", port=6379)

