from typing import List, Optional
from pydantic import BaseModel, Field, validator

# Base Models
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price_per_unit: float = Field(gt=0, description="Price must be positive")
    unit: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Wheat",
                "price_per_unit": 50.0,
                "unit": "kg"
            }
        }

class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="Quantity must be positive")

    class Config:
        schema_extra = {
            "example": {
                "product_id": 1,
                "quantity": 2
            }
        }

class Order(BaseModel):
    id: Optional[int] = None
    customer_name: str
    items: List[OrderItem]

# Request Models
class ProductCreate(BaseModel):
    name: str
    price_per_unit: float = Field(gt=0, description="Price must be positive")
    unit: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Wheat",
                "price_per_unit": 50.0,
                "unit": "kg"
            }
        }

class OrderCreate(BaseModel):
    customer_name: str
    items: List[OrderItem] = Field(..., min_items=1, description="Order must contain at least one item")

    class Config:
        schema_extra = {
            "example": {
                "customer_name": "Ravi",
                "items": [
                    {"product_id": 1, "quantity": 2},
                    {"product_id": 2, "quantity": 1}
                ]
            }
        }

# Response Models
class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float  # Calculated price (quantity * price_per_unit)

    class Config:
        schema_extra = {
            "example": {
                "product_id": 1,
                "product_name": "Wheat",
                "quantity": 2,
                "price": 100.0
            }
        }

class OrderResponse(BaseModel):
    order_id: int
    customer_name: str
    items: List[OrderItemResponse]
    total_amount: float

    class Config:
        schema_extra = {
            "example": {
                "order_id": 101,
                "customer_name": "Ravi",
                "items": [
                    {
                        "product_id": 1,
                        "product_name": "Wheat",
                        "quantity": 2,
                        "price": 100.0
                    },
                    {
                        "product_id": 2,
                        "product_name": "Rice",
                        "quantity": 1,
                        "price": 60.0
                    }
                ],
                "total_amount": 160.0
            }
        }

# Error Response Model
class ErrorResponse(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "Product with this name already exists"
            }
        }