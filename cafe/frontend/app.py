from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Service URLs
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'http://localhost:5001')
KITCHEN_SERVICE_URL = os.getenv('KITCHEN_SERVICE_URL', 'http://localhost:5002')

# Menu items with French/Italian cafe style
MENU = [
    # Coffee
    {'id': 1, 'name': 'Espresso', 'price': 3.50, 'category': 'coffee', 'icon': '☕'},
    {'id': 2, 'name': 'Cappuccino', 'price': 4.50, 'category': 'coffee', 'icon': '☕'},
    {'id': 3, 'name': 'Café Latte', 'price': 4.75, 'category': 'coffee', 'icon': '🥛'},
    {'id': 4, 'name': 'Americano', 'price': 3.75, 'category': 'coffee', 'icon': '☕'},
    {'id': 5, 'name': 'Mocha', 'price': 5.00, 'category': 'coffee', 'icon': '🍫'},
    {'id': 6, 'name': 'Macchiato', 'price': 3.75, 'category': 'coffee', 'icon': '☕'},
    
    # Pastries
    {'id': 7, 'name': 'Croissant', 'price': 3.25, 'category': 'pastry', 'icon': '🥐'},
    {'id': 8, 'name': 'Pain au Chocolat', 'price': 3.50, 'category': 'pastry', 'icon': '🥐'},
    {'id': 9, 'name': 'Éclair', 'price': 4.50, 'category': 'pastry', 'icon': '🧁'},
    {'id': 10, 'name': 'Mille-feuille', 'price': 5.25, 'category': 'pastry', 'icon': '🍰'},
    {'id': 11, 'name': 'Madeleine', 'price': 2.75, 'category': 'pastry', 'icon': '🧁'},
    {'id': 12, 'name': 'Tarte aux Fruits', 'price': 4.75, 'category': 'pastry', 'icon': '🥧'},
    
    # Ice Cream
    {'id': 13, 'name': 'Vanilla', 'price': 4.00, 'category': 'icecream', 'icon': '🍦'},
    {'id': 14, 'name': 'Chocolate', 'price': 4.00, 'category': 'icecream', 'icon': '🍦'},
    {'id': 15, 'name': 'Strawberry', 'price': 4.00, 'category': 'icecream', 'icon': '🍓'},
    {'id': 16, 'name': 'Pistachio', 'price': 4.50, 'category': 'icecream', 'icon': '🍦'},
    {'id': 17, 'name': 'Caramel', 'price': 4.25, 'category': 'icecream', 'icon': '🍮'},
    {'id': 18, 'name': 'Hazelnut', 'price': 4.50, 'category': 'icecream', 'icon': '🌰'},
    
    # Pizza
    {'id': 19, 'name': 'Margherita', 'price': 12.99, 'category': 'pizza', 'icon': '🍕'},
    {'id': 20, 'name': 'Pepperoni', 'price': 14.99, 'category': 'pizza', 'icon': '🍕'},
    {'id': 21, 'name': 'Quattro Formaggi', 'price': 15.99, 'category': 'pizza', 'icon': '🧀'},
    {'id': 22, 'name': 'Vegetariana', 'price': 13.99, 'category': 'pizza', 'icon': '🍕'},
    {'id': 23, 'name': 'Prosciutto e Funghi', 'price': 15.99, 'category': 'pizza', 'icon': '🍕'},
    {'id': 24, 'name': 'Diavola', 'price': 14.99, 'category': 'pizza', 'icon': '🌶️'},
    
    # Sandwiches
    {'id': 25, 'name': 'Croque Monsieur', 'price': 8.99, 'category': 'sandwich', 'icon': '🥪'},
    {'id': 26, 'name': 'Croque Madame', 'price': 9.99, 'category': 'sandwich', 'icon': '🥪'},
    {'id': 27, 'name': 'Italian Sub', 'price': 9.50, 'category': 'sandwich', 'icon': '🥖'},
    {'id': 28, 'name': 'Chicken Pesto', 'price': 10.50, 'category': 'sandwich', 'icon': '🥪'},
    {'id': 29, 'name': 'Caprese Panini', 'price': 8.99, 'category': 'sandwich', 'icon': '🍅'},
    {'id': 30, 'name': 'Club Sandwich', 'price': 11.99, 'category': 'sandwich', 'icon': '🥪'},
    
    # Desserts
    {'id': 31, 'name': 'Tiramisu', 'price': 6.99, 'category': 'dessert', 'icon': '🍰'},
    {'id': 32, 'name': 'Gulab Jamun', 'price': 5.50, 'category': 'dessert', 'icon': '🍡'},
    {'id': 33, 'name': 'Panna Cotta', 'price': 6.50, 'category': 'dessert', 'icon': '🍮'},
    {'id': 34, 'name': 'Crème Brûlée', 'price': 7.50, 'category': 'dessert', 'icon': '🍮'},
    {'id': 35, 'name': 'Cannoli', 'price': 5.99, 'category': 'dessert', 'icon': '🧁'},
    {'id': 36, 'name': 'Rasmalai', 'price': 6.50, 'category': 'dessert', 'icon': '🥛'},
]

@app.route('/')
def index():
    """Customer ordering page"""
    return render_template('index.html', menu=MENU)

@app.route('/kitchen')
def kitchen():
    """Kitchen management page"""
    return render_template('kitchen.html')

@app.route('/display')
def display():
    """Order status display board"""
    return render_template('display.html')

@app.route('/api/menu', methods=['GET'])
def get_menu():
    """Get menu items"""
    return jsonify(MENU), 200

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.json
        response = requests.post(f'{ORDER_SERVICE_URL}/orders', json=data)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error creating order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        response = requests.get(f'{ORDER_SERVICE_URL}/orders')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<order_number>', methods=['GET'])
def get_order(order_number):
    """Get specific order"""
    try:
        response = requests.get(f'{ORDER_SERVICE_URL}/orders/{order_number}')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error fetching order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/kitchen/orders', methods=['GET'])
def get_kitchen_orders():
    """Get kitchen orders"""
    try:
        response = requests.get(f'{KITCHEN_SERVICE_URL}/kitchen/orders')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error fetching kitchen orders: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/kitchen/orders/<order_number>/start', methods=['POST'])
def start_order(order_number):
    """Start preparing order"""
    try:
        response = requests.post(f'{KITCHEN_SERVICE_URL}/kitchen/orders/{order_number}/start')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error starting order: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/kitchen/orders/<order_number>/ready', methods=['POST'])
def ready_order(order_number):
    """Mark order as ready"""
    try:
        response = requests.post(f'{KITCHEN_SERVICE_URL}/kitchen/orders/{order_number}/ready')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error marking order ready: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/kitchen/orders/<order_number>/serve', methods=['POST'])
def serve_order(order_number):
    """Mark order as served"""
    try:
        response = requests.post(f'{KITCHEN_SERVICE_URL}/kitchen/orders/{order_number}/serve')
        return jsonify(response.json()), response.status_code
    except Exception as e:
        print(f"Error serving order: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
