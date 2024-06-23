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
    return jsonify(mobiles)

@app.route('/mobiles/<int:id>', methods=['GET'])
def get_mobile_by_id_sqlite(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query, (id,))
    mobile = cursor.fetchone()
    conn.close()
    if mobile:
        return jsonify(mobile)
    else:
        return jsonify({"message": "Mobile not found"}), 404

@app.route('/mobiles', methods=['POST'])
def add_mobile_sqlite():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO mobiles (name, price, ram, storage) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (data['name'], data['price'], data['ram'], data['storage']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mobile added successfully"})

@app.route('/mobiles/<int:id>', methods=['PUT'])
def update_mobile_sqlite(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "UPDATE mobiles SET name = ?, price = ?, ram = ?, storage = ? WHERE id = ?"
    cursor.execute(query, (data['name'], data['price'], data['ram'], data['storage'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mobile updated successfully"})

@app.route('/mobiles/<int:id>', methods=['DELETE'])
def delete_mobile_sqlite(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query_check = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query_check, (id,))
    mobile = cursor.fetchone()

    if not mobile:
        conn.close()
        return jsonify({"message": "Mobile not found for deletion"}), 404

    query_delete = "DELETE FROM mobiles WHERE id = ?"
    cursor.execute(query_delete, (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Mobile deleted successfully"})

if __name__ == '__main__':
    # Allow specifying a custom port at runtime, default to 5000
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    initialize_database()
    
    app.run(port=port, debug=True)
    print(f"Server started at port {port}")
