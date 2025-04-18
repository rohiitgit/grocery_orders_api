from typing import List, Dict
from models import Order, OrderCreate, OrderResponse, OrderItemResponse
from services.product_service import ProductService
from utils.exceptions import ProductNotFoundError, InvalidOrderError

class OrderService:
    """Service for handling order operations"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure we always use the same instance"""
        if cls._instance is None:
            cls._instance = super(OrderService, cls).__new__(cls)
            cls._instance._orders = []  # In-memory storage
            cls._instance._counter = 101  # Order ID counter (starting at 101 as per example)
            cls._instance._product_service = ProductService()  # Get product service instance
        return cls._instance
    
    def get_all_orders(self) -> List[OrderResponse]:
        """Get all orders with calculated totals and item details"""
        response_orders = []
        
        for order in self._orders:
            # Convert each order to response format with calculated prices
            response_items = []
            total_amount = 0
            
            for item in order.items:
                # Get product details
                try:
                    product = self._product_service.get_product_by_id(item.product_id)
                    
                    # Calculate item price
                    item_price = product.price_per_unit * item.quantity
                    total_amount += item_price
                    
                    # Create response item
                    response_item = OrderItemResponse(
                        product_id=item.product_id,
                        product_name=product.name,
                        quantity=item.quantity,
                        price=item_price
                    )
                    response_items.append(response_item)
                except ProductNotFoundError:
                    # Skip items with invalid product IDs in response
                    continue
            
            # Create order response
            order_response = OrderResponse(
                order_id=order.id,
                customer_name=order.customer_name,
                items=response_items,
                total_amount=total_amount
            )
            response_orders.append(order_response)
            
        return response_orders
    
    def create_order(self, order_data: OrderCreate) -> OrderResponse:
        """Create a new order
        
        Args:
            order_data: The data for the new order
            
        Returns:
            The newly created order with calculated totals
            
        Raises:
            InvalidOrderError: If the order contains invalid product IDs
        """
        # Validate product IDs
        self._validate_order_items(order_data.items)
        
        # Create new order
        new_order = Order(
            id=self._counter,
            customer_name=order_data.customer_name,
            items=order_data.items
        )
        
        # Increment counter and add to storage
        self._counter += 1
        self._orders.append(new_order)
        
        # Calculate prices and create response
        response_items = []
        total_amount = 0
        
        for item in new_order.items:
            product = self._product_service.get_product_by_id(item.product_id)
            item_price = product.price_per_unit * item.quantity
            total_amount += item_price
            
            response_item = OrderItemResponse(
                product_id=item.product_id,
                product_name=product.name,
                quantity=item.quantity,
                price=item_price
            )
            response_items.append(response_item)
        
        # Create and return order response
        order_response = OrderResponse(
            order_id=new_order.id,
            customer_name=new_order.customer_name,
            items=response_items,
            total_amount=total_amount
        )
        
        return order_response
    
    def _validate_order_items(self, items) -> None:
        """Validate that all product IDs in order items exist
        
        Args:
            items: The order items to validate
            
        Raises:
            InvalidOrderError: If any product IDs don't exist
        """
        invalid_product_ids = []
        
        for item in items:
            try:
                self._product_service.get_product_by_id(item.product_id)
            except ProductNotFoundError:
                invalid_product_ids.append(item.product_id)
        
        if invalid_product_ids:
            raise InvalidOrderError(invalid_product_ids)