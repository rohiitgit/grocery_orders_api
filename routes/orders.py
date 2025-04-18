from typing import List
from fastapi import APIRouter, HTTPException, status
from models import OrderCreate, OrderResponse, ErrorResponse
from services.order_service import OrderService
from utils.exceptions import ProductNotFoundError, InvalidOrderError

# Create router instance
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"model": ErrorResponse}}
)

# Get order service instance
order_service = OrderService()

@router.get(
    "",
    response_model=List[OrderResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all orders",
    description="Retrieve a list of all orders with calculated totals"
)
def get_all_orders():
    """
    Get all orders endpoint
    
    Returns:
        List[OrderResponse]: List of all orders with details and totals
    """
    return order_service.get_all_orders()

@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Place a new order",
    description="Create a new order with one or more products",
    responses={
        400: {"model": ErrorResponse, "description": "Invalid order data"},
        404: {"model": ErrorResponse, "description": "Product not found"}
    }
)
def create_order(order: OrderCreate):
    """
    Create a new order endpoint
    
    Args:
        order (OrderCreate): Order data with customer name and items
        
    Returns:
        OrderResponse: Created order with calculated prices and total
        
    Raises:
        HTTPException: If the order contains invalid product IDs
    """
    try:
        return order_service.create_order(order)
    except InvalidOrderError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )