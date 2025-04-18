from typing import List, Optional
from models import Product, ProductCreate
from utils.exceptions import ProductNotFoundError, ProductNameExistsError

class ProductService:
    """Service for handling product operations"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure we always use the same instance"""
        if cls._instance is None:
            cls._instance = super(ProductService, cls).__new__(cls)
            cls._instance._products = []  # In-memory storage
            cls._instance._counter = 1    # ID counter
        return cls._instance
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self._products.copy()
    
    def get_product_by_id(self, product_id: int) -> Product:
        """Get a product by ID
        
        Args:
            product_id: The ID of the product to find
            
        Returns:
            The product with the specified ID
            
        Raises:
            ProductNotFoundError: If no product with the specified ID exists
        """
        for product in self._products:
            if product.id == product_id:
                return product
        raise ProductNotFoundError(product_id)
    
    def get_product_by_name(self, name: str) -> Optional[Product]:
        """Get a product by name
        
        Args:
            name: The name of the product to find
            
        Returns:
            The product with the specified name, or None if no such product exists
        """
        for product in self._products:
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
        self._products.append(new_product)
        
        return new_product