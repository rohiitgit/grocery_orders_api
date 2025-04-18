from typing import List, Optional
import os
from models import Product, ProductCreate, ProductUpdate
from utils.exceptions import ProductNotFoundError, ProductNameExistsError
from utils.json_storage import JsonStorage

# Define path for data files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")

class ProductService:
    """Service for handling product operations"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure we always use the same instance"""
        if cls._instance is None:
            cls._instance = super(ProductService, cls).__new__(cls)
            # Initialize JSON storage
            cls._instance._storage = JsonStorage(PRODUCTS_FILE, Product)
            # Initialize counter based on existing data
            products = cls._instance._storage.read_all()
            cls._instance._counter = max([p.id for p in products], default=0) + 1
        return cls._instance
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self._storage.read_all()
    
    def get_product_by_id(self, product_id: int) -> Product:
        """Get a product by ID
        
        Args:
            product_id: The ID of the product to find
            
        Returns:
            The product with the specified ID
            
        Raises:
            ProductNotFoundError: If no product with the specified ID exists
        """
        try:
            return self._storage.get_by_id(product_id)
        except ValueError:
            raise ProductNotFoundError(product_id)
    
    def get_product_by_name(self, name: str) -> Optional[Product]:
        """Get a product by name
        
        Args:
            name: The name of the product to find
            
        Returns:
            The product with the specified name, or None if no such product exists
        """
        products = self._storage.read_all()
        for product in products:
            if product.name.lower() == name.lower():  # Case-insensitive comparison
                return product
        return None
    
    def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product
        
        Args:
            product_data: The data for the new product
            
        Returns:
            The newly created product
            
        Raises:
            ProductNameExistsError: If a product with the same name already exists
        """
        # Check name uniqueness
        existing_product = self.get_product_by_name(product_data.name)
        if existing_product:
            raise ProductNameExistsError(product_data.name)
        
        # Create new product
        new_product = Product(
            id=self._counter,
            name=product_data.name,
            price_per_unit=product_data.price_per_unit,
            unit=product_data.unit
        )
        
        # Increment counter and add to storage
        self._counter += 1
        self._storage.add_item(new_product)
        
        return new_product
        
    def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        """Update an existing product
        
        Args:
            product_id: The ID of the product to update
            product_data: The data to update the product with
            
        Returns:
            The updated product
            
        Raises:
            ProductNotFoundError: If no product with the specified ID exists
            ProductNameExistsError: If the new name already exists for another product
        """
        # Check if product exists
        self.get_product_by_id(product_id)
        
        # Check name uniqueness if name is provided
        if product_data.name is not None:
            existing_product = self.get_product_by_name(product_data.name)
            if existing_product and existing_product.id != product_id:
                raise ProductNameExistsError(product_data.name)
        
        try:
            # Update product in storage
            return self._storage.update_item(product_id, product_data.dict(exclude_unset=True))
        except ValueError:
            raise ProductNotFoundError(product_id)