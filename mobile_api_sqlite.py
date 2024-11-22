from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

# Get a database connection
def get_db_connection():
    return sqlite3.connect('mobiles.db')

# SQLite Routes

@app.route('/mobiles', methods=['GET'])
def get_mobiles_sqlite():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mobiles')
    mobiles = cursor.fetchall()
    conn.close()

    if not mobiles:
        return jsonify({"message": "No data available"}), 200
    return jsonify([{
        'id': mobile[0],
        'name': mobile[1],
        'price': mobile[2],
        'ram': mobile[3],
        'storage': mobile[4]
    } for mobile in mobiles]), 200

@app.route('/mobiles/<int:id>', methods=['GET'])
def get_mobile_by_id_sqlite(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query, (id,))
    mobile = cursor.fetchone()
    conn.close()

    if mobile:
        return jsonify({
            'id': mobile[0],
            'name': mobile[1],
            'price': mobile[2],
            'ram': mobile[3],
            'storage': mobile[4]
        }), 200
    else:
        return jsonify({"message": "Resource not found"}), 404

@app.route('/mobiles', methods=['POST'])
def add_mobile_sqlite():
    data = request.get_json()  # Assuming you're sending JSON
    print(data)  # Debugging line to check the incoming data
    if not data:
        return jsonify({"message": "No data provided"}), 400

    try:
        # Ensure that all necessary fields are present
        name = data['name']
        price = data['price']
        ram = data['ram']
        storage = data['storage']
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the mobile already exists
    query_check = 'SELECT * FROM mobiles WHERE name=? AND price=? AND ram=? AND storage=?'
    cursor.execute(query_check, (name, price, ram, storage))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "Mobile already exists"}), 400

    # Insert new mobile
    query = "INSERT INTO mobiles (name, price, ram, storage) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (name, price, ram, storage))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mobile added successfully"}), 201

@app.route('/mobiles/<int:id>', methods=['PUT'])
def update_mobile_sqlite(id):
    data = request.json
    if not data:
        return jsonify({"message": "No data provided"}), 400
    
    try:
        name = data['name']
        price = data['price']
        ram = data['ram']
        storage = data['storage']
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the mobile exists
    query_check = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query_check, (id,))
    mobile = cursor.fetchone()

    if not mobile:
        conn.close()
        return jsonify({"message": "Resource not found"}), 404

    # Update the mobile
    query = "UPDATE mobiles SET name = ?, price = ?, ram = ?, storage = ? WHERE id = ?"
    cursor.execute(query, (name, price, ram, storage, id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mobile updated successfully"}), 200

@app.route('/mobiles/<int:id>', methods=['DELETE'])
def delete_mobile_sqlite(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the mobile exists
    query_check = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query_check, (id,))
    mobile = cursor.fetchone()

    if not mobile:
        conn.close()
        return jsonify({"message": "Resource not found"}), 404

    # Delete the mobile
    query_delete = "DELETE FROM mobiles WHERE id = ?"
    cursor.execute(query_delete, (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mobile deleted successfully"}), 200

if __name__ == '__main__':
    # Allow specifying a custom port at runtime, default to 5000
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    initialize_database()
    
    app.run(port=port, debug=True)
    print(f"Server started at port {port}")
