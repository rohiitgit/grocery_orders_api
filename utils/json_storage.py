import json
import os
from typing import List, Dict, Any, TypeVar, Generic, Type
from pydantic import BaseModel

# Define a generic type for models
T = TypeVar('T', bound=BaseModel)

class JsonStorage(Generic[T]):
    """Utility class to handle JSON file storage operations for Pydantic models"""
    
    def __init__(self, file_path: str, model_class: Type[T]):
        """Initialize JsonStorage
        
        Args:
            file_path: Path to the JSON file to use for storage
            model_class: The Pydantic model class to use for type conversion
        """
        self.file_path = file_path
        self.model_class = model_class
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Create file if it doesn't exist
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump([], file)
    
    def read_all(self) -> List[T]:
        """Read all items from the JSON file
        
        Returns:
            List of items as Pydantic model instances
        """
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                return [self.model_class(**item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is empty or malformed, return empty list
            return []
    
    def write_all(self, items: List[T]) -> None:
        """Write all items to the JSON file
        
        Args:
            items: List of Pydantic model instances to write
        """
        with open(self.file_path, 'w') as file:
            # Convert Pydantic models to dictionaries
            json_data = [item.dict() for item in items]
            json.dump(json_data, file, indent=2)
    
    def add_item(self, item: T) -> T:
        """Add a new item to the JSON file
        
        Args:
            item: The Pydantic model instance to add
            
        Returns:
            The added item
        """
        items = self.read_all()
        items.append(item)
        self.write_all(items)
        return item
    
    def update_item(self, item_id: int, update_data: Dict[str, Any]) -> T:
        """Update an existing item in the JSON file
        
        Args:
            item_id: The ID of the item to update
            update_data: Dictionary with fields to update
            
        Returns:
            The updated item
            
        Raises:
            ValueError: If no item with the specified ID exists
        """
        items = self.read_all()
        
        # Find the item with the specified ID
        for i, item in enumerate(items):
            if item.id == item_id:
                # Update the item with new data (preserving fields not in update_data)
                updated_item_dict = item.dict()
                for key, value in update_data.items():
                    if value is not None:  # Only update fields with non-None values
                        updated_item_dict[key] = value
                
                # Convert back to Pydantic model
                updated_item = self.model_class(**updated_item_dict)
                
                # Replace the item in the list
                items[i] = updated_item
                
                # Write all items back to the file
                self.write_all(items)
                
                return updated_item
        
        # If no item with the specified ID exists, raise ValueError
        raise ValueError(f"No item with ID {item_id} found")
    
    def get_by_id(self, item_id: int) -> T:
        """Get an item by its ID
        
        Args:
            item_id: The ID of the item to get
            
        Returns:
            The item with the specified ID
            
        Raises:
            ValueError: If no item with the specified ID exists
        """
        items = self.read_all()
        
        for item in items:
            if item.id == item_id:
                return item
        
        raise ValueError(f"No item with ID {item_id} found")
    
    def delete_by_id(self, item_id: int) -> T:
        """Delete an item by its ID
        
        Args:
            item_id: The ID of the item to delete
            
        Returns:
            The deleted item
            
        Raises:
            ValueError: If no item with the specified ID exists
        """
        items = self.read_all()
        
        for i, item in enumerate(items):
            if item.id == item_id:
                deleted_item = items.pop(i)
                self.write_all(items)
                return deleted_item
        
        raise ValueError(f"No item with ID {item_id} found")