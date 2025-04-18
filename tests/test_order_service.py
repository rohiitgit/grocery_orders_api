import unittest
from models import ProductCreate, OrderCreate, OrderItem
from services.product_service import ProductService
from services.order_service import OrderService
from utils.exceptions import InvalidOrderError

class TestOrderService(unittest.TestCase):
    """Test cases for OrderService"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Initialize services
        self.product_service = ProductService()
        self.order_service = OrderService()
        
        # Reset the in-memory storage for clean tests
        self.product_service._products = []
        self.product_service._counter = 1
        self.order_service._orders = []
        self.order_service._counter = 101
        
        # Add test products
        self.product1 = self.product_service.create_product(
            ProductCreate(name="Product 1", price_per_unit=10.0, unit="unit")
        )
        self.product2 = self.product_service.create_product(
            ProductCreate(name="Product 2", price_per_unit=20.0, unit="kg")
        )
    
    def test_create_order(self):
        """Test creating a new order"""
        order_data = OrderCreate(
            customer_name="Test Customer",
            items=[
                OrderItem(product_id=1, quantity=2),
                OrderItem(product_id=2, quantity=1)
            ]
        )
        
        order = self.order_service.create_order(order_data)
        
        # Check order details
        self.assertEqual(order.order_id, 101)
        self.assertEqual(order.customer_name, "Test Customer")
        self.assertEqual(len(order.items), 2)
        
        # Check calculated prices
        self.assertEqual(order.items[0].price, 20.0)  # 2 * 10.0
        self.assertEqual(order.items[1].price, 20.0)  # 1 * 20.0
        self.assertEqual(order.total_amount, 40.0)  # 20.0 + 20.0
    
    def test_create_order_with_invalid_product(self):
        """Test creating an order with invalid product IDs"""
        order_data = OrderCreate(
            customer_name="Test Customer",
            items=[
                OrderItem(product_id=1, quantity=2),
                OrderItem(product_id=999, quantity=1)  # Non-existent product ID
            ]
        )
        
        # Should raise InvalidOrderError
        with self.assertRaises(InvalidOrderError):
            self.order_service.create_order(order_data)
    
    def test_get_all_orders(self):
        """Test getting all orders"""
        # Create some orders first
        order_data1 = OrderCreate(
            customer_name="Customer 1",
            items=[OrderItem(product_id=1, quantity=2)]
        )
        order_data2 = OrderCreate(
            customer_name="Customer 2",
            items=[OrderItem(product_id=2, quantity=3)]
        )
        
        self.order_service.create_order(order_data1)
        self.order_service.create_order(order_data2)
        
        orders = self.order_service.get_all_orders()
        
        # Check returned orders
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0].customer_name, "Customer 1")
        self.assertEqual(orders[1].customer_name, "Customer 2")
        
        # Check total amounts
        self.assertEqual(orders[0].total_amount, 20.0)  # 2 * 10.0
        self.assertEqual(orders[1].total_amount, 60.0)  # 3 * 20.0

if __name__ == '__main__':
    unittest.main()