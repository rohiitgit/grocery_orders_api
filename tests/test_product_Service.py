import unittest
import os
import shutil
from models import ProductCreate, ProductUpdate
from services.product_service import ProductService, DATA_DIR
from utils.exceptions import ProductNotFoundError, ProductNameExistsError

class TestProductService(unittest.TestCase):
    """Test cases for ProductService"""
    
    def setUp(self):
        """Set up test environment before each test"""
        # Create a test data directory
        self.test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data")
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        # Backup the original data dir path
        self.original_data_dir = DATA_DIR
        
        # Override the data dir path for testing
        import services.product_service
        services.product_service.DATA_DIR = self.test_data_dir
        services.product_service.PRODUCTS_FILE = os.path.join(self.test_data_dir, "products.json")
        
        # Reinitialize the service
        self.product_service = ProductService.__new__(ProductService)
        
        # Add test products
        self.test_product = self.product_service.create_product(
            ProductCreate(name="Test Product", price_per_unit=10.0, unit="unit")
        )
    
    def tearDown(self):
        """Clean up after each test"""
        # Restore the original data dir path
        import services.product_service
        services.product_service.DATA_DIR = self.original_data_dir
        services.product_service.PRODUCTS_FILE = os.path.join(self.original_data_dir, "products.json")
        
        # Remove the test data directory
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
    
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
    
    def test_update_product(self):
        """Test updating a product"""
        # Update just the price
        updated_product = self.product_service.update_product(
            self.test_product.id,
            ProductUpdate(price_per_unit=15.0)
        )
        self.assertEqual(updated_product.id, self.test_product.id)
        self.assertEqual(updated_product.name, "Test Product")
        self.assertEqual(updated_product.price_per_unit, 15.0)
        self.assertEqual(updated_product.unit, "unit")
        
        # Update multiple fields
        updated_product = self.product_service.update_product(
            self.test_product.id,
            ProductUpdate(name="Updated Product", unit="box")
        )
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.unit, "box")
        self.assertEqual(updated_product.price_per_unit, 15.0)  # Should keep the previously updated price
        
        # Test invalid ID
        with self.assertRaises(ProductNotFoundError):
            self.product_service.update_product(999, ProductUpdate(name="Invalid"))
        
        # Test duplicate name
        self.product_service.create_product(
            ProductCreate(name="Another Product", price_per_unit=20.0, unit="kg")
        )
        with self.assertRaises(ProductNameExistsError):
            self.product_service.update_product(
                self.test_product.id,
                ProductUpdate(name="Another Product")
            )
            
    def test_json_persistence(self):
        """Test that products are persisted to JSON file"""
        # Create a new product
        new_product = self.product_service.create_product(
            ProductCreate(name="Persistent Product", price_per_unit=25.0, unit="lb")
        )
        
        # Create a new service instance (which should read from the JSON file)
        new_service = ProductService.__new__(ProductService)
        
        # Verify the product was persisted
        products = new_service.get_all_products()
        self.assertEqual(len(products), 3)  # 1 from setUp + 2 from tests
        
        # Find the new product
        persisted_product = None
        for product in products:
            if product.id == new_product.id:
                persisted_product = product
                break
        
        self.assertIsNotNone(persisted_product)
        self.assertEqual(persisted_product.name, "Persistent Product")
        self.assertEqual(persisted_product.price_per_unit, 25.0)

if __name__ == '__main__':
    unittest.main()