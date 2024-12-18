from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import date

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logger configuration
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

log_file = os.path.join(logs_dir, f'{date.today()}.log')

log_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Delete older log files (keeping only the latest 5 log files)
for filename in os.listdir(logs_dir):
    if filename.endswith('.log'):
        filepath = os.path.join(logs_dir, filename)
        if filepath != log_file:
            os.remove(filepath)

# SQLite Database Initialization
def initialize_database():
    conn = sqlite3.connect('mobiles.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mobiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            ram TEXT,
            storage TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database initialized or already exists.")

# Get a database connection
def get_db_connection():
    return sqlite3.connect('mobiles.db')

# SQLite Routes

@app.route('/')
def hello_world():
    message = {
        "greeting": "Hello, World!",
        "welcome_message": "Welcome to our Flask API service!",
        "service_status": "The service is currently up and running without issues.",
        "note": "You can explore various API endpoints for more features.",
        "support_contact": "If you need help, contact us at support@example.com."
    }
    return jsonify(message), 200



@app.route('/mobiles', methods=['GET'])
def get_mobiles_sqlite():
    logger.info("Fetching all mobiles from the database.")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mobiles')
    mobiles = cursor.fetchall()
    conn.close()

    if not mobiles:
        logger.info("No mobiles found in the database.")
        return jsonify({"message": "No data available"}), 200
    
    logger.info(f"Found {len(mobiles)} mobiles in the database.")
    return jsonify([{
        'id': mobile[0],
        'name': mobile[1],
        'price': mobile[2],
        'ram': mobile[3],
        'storage': mobile[4]
    } for mobile in mobiles]), 200

@app.route('/mobiles/<int:id>', methods=['GET'])
def get_mobile_by_id_sqlite(id):
    logger.info(f"Fetching mobile with ID {id}.")
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query, (id,))
    mobile = cursor.fetchone()
    conn.close()

    if mobile:
        logger.info(f"Mobile with ID {id} found.")
        return jsonify({
            'id': mobile[0],
            'name': mobile[1],
            'price': mobile[2],
            'ram': mobile[3],
            'storage': mobile[4]
        }), 200
    else:
        logger.warning(f"Mobile with ID {id} not found.")
        return jsonify({"message": "Resource not found"}), 404

@app.route('/mobiles', methods=['POST'])
def add_mobile_sqlite():
    data = request.get_json()  # Assuming you're sending JSON
    logger.info(f"Received data for new mobile: {data}")  # Logging the incoming data
    if not data:
        logger.warning("No data provided in the request.")
        return jsonify({"message": "No data provided"}), 400

    try:
        # Ensure that all necessary fields are present
        name = data['name']
        price = data['price']
        ram = data['ram']
        storage = data['storage']
    except KeyError as e:
        logger.error(f"Missing field in request: {e}")
        return jsonify({"error": f"Missing field: {e}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the mobile already exists
    query_check = 'SELECT * FROM mobiles WHERE name=? AND price=? AND ram=? AND storage=?'
    cursor.execute(query_check, (name, price, ram, storage))
    if cursor.fetchone():
        conn.close()
        logger.warning(f"Mobile already exists: {name}, {price}, {ram}, {storage}")
        return jsonify({"error": "Mobile already exists"}), 400

    # Insert new mobile
    query = "INSERT INTO mobiles (name, price, ram, storage) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (name, price, ram, storage))
    conn.commit()
    conn.close()

    logger.info(f"Mobile added successfully: {name}, {price}, {ram}, {storage}")
    return jsonify({"message": "Mobile added successfully"}), 201

@app.route('/mobiles/<int:id>', methods=['PUT'])
def update_mobile_sqlite(id):
    data = request.json
    if not data:
        logger.warning(f"No data provided for update (ID: {id}).")
        return jsonify({"message": "No data provided"}), 400
    
    try:
        name = data['name']
        price = data['price']
        ram = data['ram']
        storage = data['storage']
    except KeyError as e:
        logger.error(f"Missing field in update request (ID: {id}): {e}")
        return jsonify({"error": f"Missing field: {e}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the mobile exists
    query_check = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query_check, (id,))
    mobile = cursor.fetchone()

    if not mobile:
        conn.close()
        logger.warning(f"Mobile not found for update (ID: {id})")
        return jsonify({"message": "Resource not found"}), 404

    # Update the mobile
    query = "UPDATE mobiles SET name = ?, price = ?, ram = ?, storage = ? WHERE id = ?"
    cursor.execute(query, (name, price, ram, storage, id))
    conn.commit()
    conn.close()

    logger.info(f"Mobile updated successfully (ID: {id})")
    return jsonify({"message": "Mobile updated successfully"}), 200

@app.route('/mobiles/<int:id>', methods=['DELETE'])
def delete_mobile_sqlite(id):
    logger.info(f"Attempting to delete mobile with ID {id}.")
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the mobile exists
    query_check = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query_check, (id,))
    mobile = cursor.fetchone()

    if not mobile:
        conn.close()
        logger.warning(f"Mobile with ID {id} not found for deletion.")
        return jsonify({"message": "Resource not found"}), 404

    # Delete the mobile
    query_delete = "DELETE FROM mobiles WHERE id = ?"
    cursor.execute(query_delete, (id,))
    conn.commit()
    conn.close()

    logger.info(f"Mobile deleted successfully (ID: {id})")
    return jsonify({"message": "Mobile deleted successfully"}), 200

if __name__ == '__main__':
    # Allow specifying a custom port at runtime, default to 5000
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    initialize_database()
    
    app.run(port=port, debug=True)
    logger.info(f"Server started at port {port}")

# 1. **Run Flask App with Default Port (5000)**:
# Run without specifying a port, defaults to 5000:
# python Mobile_api_flask_sqlite.py

# 2. **Run Flask App with a Custom Port**:
# Specify a custom port (e.g., 8000):
# python Mobile_api_flask_sqlite.py 8000
