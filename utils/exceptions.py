class ProductNotFoundError(Exception):
    """Raised when a product is not found"""
    def __init__(self, product_id: int):
        self.product_id = product_id
        self.message = f"Product with ID {product_id} not found"
        super().__init__(self.message)

class ProductNameExistsError(Exception):
    """Raised when trying to create a product with a name that already exists"""
    def __init__(self, name: str):
        self.name = name
        self.message = f"Product with name '{name}' already exists"
        super().__init__(self.message)

class InvalidOrderError(Exception):
    """Raised when an order contains invalid product IDs"""
    def __init__(self, invalid_product_ids: list):
        self.invalid_product_ids = invalid_product_ids
        self.message = f"Invalid product IDs: {', '.join(map(str, invalid_product_ids))}"
        super().__init__(self.message)