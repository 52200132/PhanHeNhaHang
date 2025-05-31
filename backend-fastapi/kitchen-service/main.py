from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import kitchen_order_routes
from utils.logger import get_logger

# Create logger for this module
logger = get_logger(__name__)

app = FastAPI(title="Kitchen Service API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(kitchen_order_routes.router, prefix="/api/v1", tags=["kitchen_orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Kitchen Service API"}