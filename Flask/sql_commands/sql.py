import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('bme680_data.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS bme680_data (
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    pressure REAL,
    humidity REAL,
    gas_resistance REAL
    battery_level REAL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()