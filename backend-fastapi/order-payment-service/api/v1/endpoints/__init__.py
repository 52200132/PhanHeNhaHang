from api.v1.endpoints.table_routes import router as table_router
from api.v1.endpoints.shift_routes import router as shift_router
from api.v1.endpoints.order_routes import router as order_router

__all__ = ["table_router", "shift_router", "order_router"]
