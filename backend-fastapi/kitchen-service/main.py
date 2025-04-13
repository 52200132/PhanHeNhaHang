from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from models import KitchenOrder
from api.v1.endpoints import kitchen_order_routes

app = FastAPI(title="Kitchen Service API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
async def startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database kitchen service connected and tables created.")
    except Exception as e:
        print(f"Database Error: {e}")

# Include routers
app.include_router(kitchen_order_routes.router, prefix="/api/v1", tags=["kitchen_orders"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Kitchen Service API"}