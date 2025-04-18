import unittest
import os
import shutil
from models import ProductCreate, OrderCreate, OrderItem
from services.product_service import ProductService, DATA_DIR as PRODUCT_DATA_DIR
from services.order_service import OrderService, DATA_DIR as ORDER_DATA_DIR
from utils.exceptions import InvalidOrderError

class TestOrderService(unittest.TestCase):
    """Test cases for OrderService"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Create a test data directory
        self.test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data")
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Backup the original data dir paths
        self.original_product_data_dir = PRODUCT_DATA_DIR
        self.original_order_data_dir = ORDER_DATA_DIR
        
        # Override the data dir paths for testing
        import services.product_service
        import services.order_service
        
        services.product_service.DATA_DIR = self.test_data_dir
        services.product_service.PRODUCTS_FILE = os.path.join(self.test_data_dir, "products.json")
        
        services.order_service.DATA_DIR = self.test_data_dir
        services.order_service.ORDERS_FILE = os.path.join(self.test_data_dir, "orders.json")
        
        # Reinitialize the services
        self.product_service = ProductService.__new__(ProductService)
        self.order_service = OrderService.__new__(OrderService)
        
        # Add test products
        self.product1 = self.product_service.create_product(
            ProductCreate(name="Product 1", price_per_unit=10.0, unit="unit")
        )
        self.product2 = self.product_service.create_product(
            ProductCreate(name="Product 2", price_per_unit=20.0, unit="kg")
        )
    
    def tearDown(self):
        """Clean up after each test"""
        # Restore the original data dir paths
        import services.product_service
        import services.order_service
        
        services.product_service.DATA_DIR = self.original_product_data_dir
        services.product_service.PRODUCTS_FILE = os.path.join(self.original_product_data_dir, "products.json")
        
        services.order_service.DATA_DIR = self.original_order_data_dir
        services.order_service.ORDERS_FILE = os.path.join(self.original_order_data_dir, "orders.json")
        
        # Remove the test data directory
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
    
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
        
    def test_json_persistence(self):
        """Test that orders are persisted to JSON file"""
        # Create a new order
        order_data = OrderCreate(
            customer_name="Persistent Customer",
            items=[
                OrderItem(product_id=1, quantity=3),
                OrderItem(product_id=2, quantity=2)
            ]
        )
        order = self.order_service.create_order(order_data)
        
        # Create a new service instance (which should read from the JSON file)
        new_order_service = OrderService.__new__(OrderService)
        
        # Verify the order was persisted
        orders = new_order_service.get_all_orders()
        self.assertEqual(len(orders), 1)
        
        # Check order details
        persisted_order = orders[0]
        self.assertEqual(persisted_order.order_id, order.order_id)
        self.assertEqual(persisted_order.customer_name, "Persistent Customer")
        self.assertEqual(len(persisted_order.items), 2)
        
        # Check calculated prices
        self.assertEqual(persisted_order.total_amount, 70.0)  # (3 * 10.0) + (2 * 20.0)

if __name__ == '__main__':
    unittest.main()