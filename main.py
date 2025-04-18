from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import products, orders
from utils.exceptions import ProductNotFoundError, ProductNameExistsError, InvalidOrderError
from models import ErrorResponse

# Create FastAPI application
app = FastAPI(
    title="Smart Grocery Order API System",
    description="A RESTful API for a basic grocery ordering system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(products.router)
app.include_router(orders.router)

# Exception handlers
@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    """Handle product not found errors"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message}
    )

@app.exception_handler(ProductNameExistsError)
async def product_name_exists_handler(request: Request, exc: ProductNameExistsError):
    """Handle product name exists errors"""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message}
    )

@app.exception_handler(InvalidOrderError)
async def invalid_order_handler(request: Request, exc: InvalidOrderError):
    """Handle invalid order errors"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message}
    )

# Root endpoint
@app.get(
    "/",
    tags=["root"],
    summary="Root endpoint",
    description="Welcome message and API information"
)
async def root():
    """
    Root endpoint handler
    
    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "Welcome to the Smart Grocery Order API System",
        "version": "1.0.0",
        "documentation": "/docs"
    }

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)