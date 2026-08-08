import sqlite3

# Connect to the SQLite database (or create it if not exists)
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Define the SQL query to create a table
create_table_query = '''
CREATE TABLE IF NOT EXISTS mobiles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL,
    ram INTEGER,
    storage INTEGER
)
'''

# Execute the create table query
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'mobiles' created successfully.")
