from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from models import Dish, Category, Ingredient
from api.v1.endpoints import dish_routes, category_routes, ingredient_routes, recipe_routes

app = FastAPI(title="Menu Service API")

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
        print("Database menu service connected and tables created.")
    except Exception as e:
        print(f"Database Error: {e}")

# Include routers
app.include_router(dish_routes.router, prefix="/api/v1", tags=["dishes"])
app.include_router(category_routes.router, prefix="/api/v1", tags=["categories"])
app.include_router(ingredient_routes.router, prefix="/api/v1", tags=["ingredients"])
app.include_router(recipe_routes.router, prefix="/api/v1", tags=["recipes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Menu Service API"}