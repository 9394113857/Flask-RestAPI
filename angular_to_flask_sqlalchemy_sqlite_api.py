from flask import Flask, request, jsonify
from flask_cors import CORS  # Cross-Origin Resource Sharing (CORS) for handling API requests from different origins
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy for ORM (Object-Relational Mapping)
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes (allowing cross-origin requests from the Angular app)
CORS(app)

# Set up logger configuration to store logs in a 'logs' folder
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)  # Create 'logs' directory if it doesn't exist

# Create a timestamp for unique log file names
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Define log file name with timestamp
log_file = os.path.join(logs_dir, f'{timestamp}.log')

# Set up rotating log handler to manage log file size (max 1MB, keeping 5 backups)
log_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s'))  # Log format

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set logging level to INFO
logger.addHandler(log_handler)  # Add rotating file handler for logging

# Clean up old log files (delete logs except the latest one)
for filename in os.listdir(logs_dir):
    if filename.endswith('.log'):
        filepath = os.path.join(logs_dir, filename)
        # Skip the current log file that's in use
        if filepath != log_file:  
            try:
                os.remove(filepath)
                logger.info(f"Deleted old log file: {filename}")
            except PermissionError as e:
                logger.error(f"PermissionError: Could not delete file {filename} because it's in use. Error: {e}")

# Set up Flask-SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mobiles.db'  # Define SQLite database URI (mobiles.db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
db = SQLAlchemy(app)  # Initialize SQLAlchemy instance with Flask app

# Define the Mobile model class for SQLAlchemy ORM
class Mobile(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Define the 'id' column as the primary key
    name = db.Column(db.String(100), nullable=False)  # 'name' column with a max length of 100 characters
    price = db.Column(db.Float)  # 'price' column with a float data type
    ram = db.Column(db.String(50))  # 'ram' column with a max length of 50 characters
    storage = db.Column(db.String(50))  # 'storage' column with a max length of 50 characters

    # Method to represent the object as a string (useful for debugging)
    def __repr__(self):
        return f"<Mobile {self.name}>"

# Routes for handling CRUD operations

# Route to return "Hello, World!" in JSON format
@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

# Route to get all mobiles from the database
@app.route('/mobiles', methods=['GET'])
def get_mobiles_sqlalchemy():
    logger.info("Fetching all mobiles from the database.")
    
    # Query all records from the Mobile table
    mobiles = Mobile.query.all()
    
    if not mobiles:
        logger.info("No mobiles found in the database.")
        return jsonify({"message": "No data available"}), 200  # Return a message if no records are found
    
    logger.info(f"Found {len(mobiles)} mobiles in the database.")
    # Return a list of mobiles as JSON
    return jsonify([{
        'id': mobile.id,
        'name': mobile.name,
        'price': mobile.price,
        'ram': mobile.ram,
        'storage': mobile.storage
    } for mobile in mobiles]), 200

# Route to get a single mobile by its ID
@app.route('/mobiles/<int:id>', methods=['GET'])
def get_mobile_by_id_sqlalchemy(id):
    logger.info(f"Fetching mobile with ID {id}.")
    
    # Query the Mobile table for a record with the specified ID
    mobile = Mobile.query.get(id)

    if mobile:
        logger.info(f"Mobile with ID {id} found.")
        # Return the mobile data as JSON if found
        return jsonify({
            'id': mobile.id,
            'name': mobile.name,
            'price': mobile.price,
            'ram': mobile.ram,
            'storage': mobile.storage
        }), 200
    else:
        logger.warning(f"Mobile with ID {id} not found.")
        # Return an error message if the mobile is not found
        return jsonify({"message": "Resource not found"}), 404

# Route to add a new mobile
@app.route('/mobiles', methods=['POST'])
def add_mobile_sqlalchemy():
    data = request.get_json()  # Parse the incoming JSON data
    logger.info(f"Received data for new mobile: {data}")  # Log the incoming data
    
    if not data:
        logger.warning("No data provided in the request.")
        return jsonify({"message": "No data provided"}), 400  # Return error if no data is provided

    try:
        # Extract necessary fields from the incoming data
        name = data['name']
        price = data['price']
        ram = data['ram']
        storage = data['storage']
    except KeyError as e:
        logger.error(f"Missing field in request: {e}")
        return jsonify({"error": f"Missing field: {e}"}), 400  # Return error if any field is missing

    # Check if a mobile with the same details already exists
    existing_mobile = Mobile.query.filter_by(name=name, price=price, ram=ram, storage=storage).first()
    if existing_mobile:
        logger.warning(f"Mobile already exists: {name}, {price}, {ram}, {storage}")
        return jsonify({"error": "Mobile already exists"}), 400  # Return error if the mobile already exists

    # Create a new Mobile object and add it to the session
    new_mobile = Mobile(name=name, price=price, ram=ram, storage=storage)
    db.session.add(new_mobile)  # Add the new mobile to the database session
    db.session.commit()  # Commit the transaction to the database

    logger.info(f"Mobile added successfully: {name}, {price}, {ram}, {storage}")
    return jsonify({"message": "Mobile added successfully"}), 201  # Return success message

# Route to update an existing mobile
@app.route('/mobiles/<int:id>', methods=['PUT'])
def update_mobile_sqlalchemy(id):
    data = request.json  # Parse the incoming JSON data
    if not data:
        logger.warning(f"No data provided for update (ID: {id}).")
        return jsonify({"message": "No data provided"}), 400  # Return error if no data is provided
    
    try:
        # Extract necessary fields from the incoming data
        name = data['name']
        price = data['price']
        ram = data['ram']
        storage = data['storage']
    except KeyError as e:
        logger.error(f"Missing field in update request (ID: {id}): {e}")
        return jsonify({"error": f"Missing field: {e}"}), 400  # Return error if any field is missing

    # Query the Mobile table for the mobile with the specified ID
    mobile = Mobile.query.get(id)

    if not mobile:
        logger.warning(f"Mobile not found for update (ID: {id})")
        return jsonify({"message": "Resource not found"}), 404  # Return error if mobile is not found

    # Update the mobile details
    mobile.name = name
    mobile.price = price
    mobile.ram = ram
    mobile.storage = storage
    db.session.commit()  # Commit the changes to the database

    logger.info(f"Mobile updated successfully (ID: {id})")
    return jsonify({"message": "Mobile updated successfully"}), 200  # Return success message

# Route to delete a mobile by ID
@app.route('/mobiles/<int:id>', methods=['DELETE'])
def delete_mobile_sqlalchemy(id):
    logger.info(f"Attempting to delete mobile with ID {id}.")
    
    # Query the Mobile table for the mobile with the specified ID
    mobile = Mobile.query.get(id)

    if not mobile:
        logger.warning(f"Mobile with ID {id} not found for deletion.")
        return jsonify({"message": "Resource not found"}), 404  # Return error if mobile is not found

    db.session.delete(mobile)  # Delete the mobile from the database session
    db.session.commit()  # Commit the changes to the database

    logger.info(f"Mobile deleted successfully (ID: {id})")
    return jsonify({"message": "Mobile deleted successfully"}), 200  # Return success message

# Main entry point for the Flask app
if __name__ == '__main__':
    # Allow specifying a custom port at runtime, default to 5000
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    
    # Ensure app context is active when calling db.create_all()
    with app.app_context():
        db.create_all()  # Create all tables if they don't already exist

    # Run the Flask app on the specified port
    app.run(port=port, debug=True)
    logger.info(f"Server started at port {port}")




# Build the Docker image from the current directory (use the Dockerfile in the directory)
#docker build -t flask-sqlalchemy-app .  # -t assigns a name (flask-sqlalchemy-app) to the image

# Run the Docker container, mapping the host port 5000 to the container's port 5000
#docker run -p 5000:5000 flask-sqlalchemy-app  # -p maps the container port (5000) to your local machine port (5000)

# Optional: Run the container on a custom port (e.g., 8080 on your host machine)
#docker run -p 8080:5000 flask-sqlalchemy-app  # Here, port 5000 inside the container is mapped to port 8080 on your host

