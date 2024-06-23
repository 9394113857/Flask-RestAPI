from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# SQLite Configuration
DATABASE = 'mobiles.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Create the mobiles table if it doesn't exist
with app.app_context():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mobiles (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            ram INTEGER,
            storage INTEGER
        )
    ''')
    db.commit()

# SQLite Routes

@app.route('/mobiles', methods=['GET'])
def get_mobiles_sqlite():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM mobiles')
    mobiles = cursor.fetchall()
    return jsonify([dict(row) for row in mobiles])

@app.route('/mobiles/<int:id>', methods=['GET'])
def get_mobile_by_id_sqlite(id):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM mobiles WHERE id = ?"
    cursor.execute(query, (id,))
    mobile = cursor.fetchone()
    if mobile:
        return jsonify(dict(mobile))
    else:
        return jsonify({"message": "Mobile not found"}), 404

@app.route('/mobiles', methods=['POST'])
def add_mobile_sqlite():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    query = "INSERT INTO mobiles (name, price, ram, storage) VALUES (?, ?, ?, ?)"
    cursor.execute(query, (data['name'], data['price'], data['ram'], data['storage']))
    db.commit()
    return jsonify({"message": "Mobile added successfully"})

@app.route('/mobiles/<int:id>', methods=['PUT'])
def update_mobile_sqlite(id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    query = "UPDATE mobiles SET name = ?, price = ?, ram = ?, storage = ? WHERE id = ?"
    cursor.execute(query, (data['name'], data['price'], data['ram'], data['storage'], id))
    db.commit()
    return jsonify({"message": "Mobile updated successfully"})

@app.route('/mobiles/<int:id>', methods=['DELETE'])
def delete_mobile_sqlite(id):
    db = get_db()
    cursor = db.cursor()
    query = "DELETE FROM mobiles WHERE id = ?"
    cursor.execute(query, (id,))
    db.commit()
    return jsonify({"message": "Mobile deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
