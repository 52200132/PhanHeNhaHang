from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import table_routes, shift_routes, order_routes

# from utils.logger import get_logger

# logger = get_logger(__name__)

app = FastAPI(title="Order Payment Service API")

# Cấu hình CORS để cho phép các client gọi API từ các nguồn khác
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# def startup():
#     try:
#         # Tạo bảng trong database (nếu chưa tồn tại)
#         Base.metadata.create_all(bind=engine)
#         print("Database connected and tables created.")
#     except Exception as e:
#         print(f"Database Error: {e}")

# Đăng ký các router
app.include_router(table_routes.router, prefix="/api/v1")
app.include_router(shift_routes.router, prefix="/api/v1")
app.include_router(order_routes.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Order Payment Service API"}