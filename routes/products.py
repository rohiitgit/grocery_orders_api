from typing import List
from fastapi import APIRouter, HTTPException, status
from models import Product, ProductCreate, ProductUpdate, ErrorResponse
from services.product_service import ProductService
from utils.exceptions import ProductNameExistsError, ProductNotFoundError

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

@router.put(
    "/{product_id}",
    response_model=Product,
    status_code=status.HTTP_200_OK,
    summary="Update a product",
    description="Update an existing product's information",
    responses={
        404: {"model": ErrorResponse, "description": "Product not found"},
        409: {"model": ErrorResponse, "description": "Product with this name already exists"}
    }
)
def update_product(product_id: int, product: ProductUpdate):
    """
    Update a product endpoint
    
    Args:
        product_id (int): ID of the product to update
        product (ProductUpdate): Updated product data
        
    Returns:
        Product: Updated product
        
    Raises:
        HTTPException: If product not found or name conflict
    """
    try:
        return product_service.update_product(product_id, product)
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except ProductNameExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )