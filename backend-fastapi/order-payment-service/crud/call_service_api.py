import requests

from config import KITCHEN_SERVICE_URL

def call_create_kitchen_order_api(order_id: int, dish_id: int, note: str, quantity: int):
    """
    Gọi API để tạo đơn hàng trong bếp
    """
    url = f"{KITCHEN_SERVICE_URL}/kitchen_orders"
    payload = {
        "order_id": order_id,
        "dish_id": dish_id,
        "note": note,
        "quantity": quantity
    }
    response = requests.post(url, json=payload)
