import unittest
from models import ProductCreate
from services.product_service import ProductService
from utils.exceptions import ProductNotFoundError, ProductNameExistsError

class TestProductService(unittest.TestCase):
    """Test cases for ProductService"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.product_service = ProductService()
        # Reset the in-memory storage for clean tests
        self.product_service._products = []
        self.product_service._counter = 1
        
        # Add test products
        self.test_product = self.product_service.create_product(
            ProductCreate(name="Test Product", price_per_unit=10.0, unit="unit")
        )
    
    def test_get_all_products(self):
        """Test getting all products"""
        products = self.product_service.get_all_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Test Product")
    
    def test_get_product_by_id(self):
        """Test getting a product by ID"""
        product = self.product_service.get_product_by_id(self.test_product.id)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price_per_unit, 10.0)
        
        # Test non-existent product
        with self.assertRaises(ProductNotFoundError):
            self.product_service.get_product_by_id(999)
    
    def test_get_product_by_name(self):
        """Test getting a product by name"""
        product = self.product_service.get_product_by_name("Test Product")
        self.assertIsNotNone(product)
        self.assertEqual(product.id, self.test_product.id)
        
        # Test case insensitivity
        product = self.product_service.get_product_by_name("test product")
        self.assertIsNotNone(product)
        
        # Test non-existent product
        product = self.product_service.get_product_by_name("Non-existent Product")
        self.assertIsNone(product)
    
    def test_create_product(self):
        """Test creating a new product"""
        new_product = self.product_service.create_product(
            ProductCreate(name="New Product", price_per_unit=20.0, unit="kg")
        )
        self.assertEqual(new_product.id, 2)  # Should be the next ID
        self.assertEqual(new_product.name, "New Product")
        
        # Test duplicate name
        with self.assertRaises(ProductNameExistsError):
            self.product_service.create_product(
                ProductCreate(name="Test Product", price_per_unit=30.0, unit="box")
            )

if __name__ == '__main__':
    unittest.main()