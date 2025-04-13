from httpx import Client
from config import MENU_SERVICE_URL
from utils.logger import get_logger

logger = get_logger(__name__)

def get_dish_price(client: Client, dish_id: int) -> float:
    """
    Lấy giá của món ăn từ Menu Service.
    Trả về giá mặc định là 1 nếu không lấy được thông tin.
    """
    try:
        response = client.get(f"{MENU_SERVICE_URL}/dishes/{dish_id}")
        if response.status_code == 200:
            dish_data = response.json()
            dish_price = dish_data.get("price", 1)
            logger.info(f"Fetched dish price: {dish_price} for dish_id: {dish_id}")
            return dish_price
        else:
            logger.warning(f"Failed to fetch dish details for dish_id {dish_id}, using default price: 1")
            return 1
    except Exception as e:
        logger.error(f"Error getting dish price for dish_id {dish_id}: {e}. Using default price: 1")
        return 1
