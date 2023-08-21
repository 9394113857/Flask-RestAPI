from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import sys

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and websites:

# MySQL Configuration
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='raghu',
    database='nodejs_db'
)
mysql_cursor = mysql_conn.cursor(dictionary=True)

# MySQL Routes

@app.route('/mobiles', methods=['GET'])
def get_mobiles_mysql():
    mysql_cursor.execute('SELECT * FROM mobiles')
    mobiles = mysql_cursor.fetchall() 
    return jsonify(mobiles)

@app.route('/mobiles/<int:id>', methods=['GET']) 
def get_mobile_by_id_mysql(id): 
    query = "SELECT * FROM mobiles WHERE id = %s"
    mysql_cursor.execute(query, (id,))
    mobile = mysql_cursor.fetchone()
    if mobile:
        return jsonify(mobile)
    else:
        return jsonify({"message": "Mobile not found"}), 404

@app.route('/mobiles', methods=['POST'])
def add_mobile_mysql():
    data = request.json
    query = "INSERT INTO mobiles (name, price, ram, storage) VALUES (%s, %s, %s, %s)"
    mysql_cursor.execute(query, (data['name'], data['price'], data['ram'], data['storage']))
    mysql_conn.commit()
    return jsonify({"message": "Mobile added successfully"})

@app.route('/mobiles/<int:id>', methods=['PUT'])
def update_mobile_mysql(id):
    data = request.json
    query = "UPDATE mobiles SET name = %s, price = %s, ram = %s, storage = %s WHERE id = %s"
    mysql_cursor.execute(query, (data['name'], data['price'], data['ram'], data['storage'], id))
    mysql_conn.commit()
    return jsonify({"message": "Mobile updated successfully"})

@app.route('/mobiles/<int:id>', methods=['DELETE'])
def delete_mobile_mysql(id):
    query = "DELETE FROM mobiles WHERE id = %s"
    mysql_cursor.execute(query, (id,))
    mysql_conn.commit()
    return jsonify({"message": "Mobile deleted successfully"})

if __name__ == '__main__':
    # Allow specifying a custom port at runtime, default to 5000
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    app.run(port=port, debug=True)
    print(f"Server started at port {port}")


# python app.py 6001

# This will start the server on port 6001 and print "Server started at port 6001" in the console. 
# If no argument is provided, it will run on port 5000 by default.

