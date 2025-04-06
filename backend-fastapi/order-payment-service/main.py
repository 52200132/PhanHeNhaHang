from fastapi import FastAPI
# from api.v1.endpoints import user_routes
from db import engine, Base
from models import Table, Order, Payment, OrderDetail, Shift

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database connected and tables created.")
    except Exception as e:
        print(f"Database Error: {e}")
        
# app.include_router(user_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Service 1 API"}