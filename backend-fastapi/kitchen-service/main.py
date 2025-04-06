from fastapi import FastAPI
# from api.v1.endpoints import user_routes
from db import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

# app.include_router(user_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Service 1 API"}