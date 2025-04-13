from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from api.v1.endpoints import dish_routes, category_routes, ingredient_routes, recipe_routes
from utils.logger import default_logger

logger = default_logger

app = FastAPI(title="Menu Service API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dish_routes.router, prefix="/api/v1", tags=["dishes"])
app.include_router(category_routes.router, prefix="/api/v1", tags=["categories"])
app.include_router(ingredient_routes.router, prefix="/api/v1", tags=["ingredients"])
app.include_router(recipe_routes.router, prefix="/api/v1", tags=["recipes"])

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    result = []
    for error in exc.errors():
        error_dict = {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
        }
        result.append(error_dict)
    logger.error(f"Validation error: {result}")
    return JSONResponse(
        status_code=400,
        content=({"detail": result})
    )

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Menu Service API"}

@app.on_event("startup")
async def startup_event():
    logger.info("Menu Service starting up")