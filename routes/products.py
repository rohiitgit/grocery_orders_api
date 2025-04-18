from typing import List
from fastapi import APIRouter, HTTPException, status
from models import Product, ProductCreate, ErrorResponse
from services.product_service import ProductService
from utils.exceptions import ProductNameExistsError

# Create router instance
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"model": ErrorResponse}}
)

# Get product service instance
product_service = ProductService()

@router.get(
    "",
    response_model=List[Product],
    status_code=status.HTTP_200_OK,
    summary="Get all products",
    description="Retrieve a list of all available products"
)
def get_all_products():
    """
    Get all products endpoint
    
    Returns:
        List[Product]: List of all products
    """
    return product_service.get_all_products()

@router.post(
    "",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new product",
    description="Add a new product to the catalog",
    responses={
        409: {"model": ErrorResponse, "description": "Product with this name already exists"}
    }
)
def create_product(product: ProductCreate):
    """
    Create a new product endpoint
    
    Args:
        product (ProductCreate): Product data
        
    Returns:
        Product: Created product
        
    Raises:
        HTTPException: If a product with the same name already exists
    """
    try:
        return product_service.create_product(product)
    except ProductNameExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )