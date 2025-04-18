# Smart Grocery Order API System

A RESTful API backend for a grocery ordering system built with FastAPI.

## Features

- Product management (add, view)
- Order processing (place, view)
- Automatic order calculation
- Input validation and error handling
- RESTful API design
- Auto-generated API documentation

## Project Structure

```
project/
├── main.py (API entry point)
├── models.py (Data classes)
├── routes/
│   ├── __init__.py
│   ├── products.py
│   └── orders.py
├── services/
│   ├── __init__.py
│   ├── product_service.py
│   └── order_service.py
├── utils/
│   ├── __init__.py
│   └── exceptions.py
└── README.md
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic

## Installation

1. Clone the repository or download the source code

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

## Running the Application

1. Start the server:
   ```bash
   python main.py
   ```
   
   Or using Uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

2. Access the API at http://localhost:8000

3. Access the API documentation at http://localhost:8000/docs

## API Endpoints

### Products

- `GET /products` - List all products
- `POST /products` - Add a new product

### Orders

- `GET /orders` - List all orders with details
- `POST /orders` - Place a new order

## Example Usage

### Adding a Product

```bash
curl -X 'POST' \
  'http://localhost:8000/products' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Wheat",
  "price_per_unit": 50,
  "unit": "kg"
}'
```

### Placing an Order

```bash
curl -X 'POST' \
  'http://localhost:8000/orders' \
  -H 'Content-Type: application/json' \
  -d '{
  "customer_name": "Ravi",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}'
```