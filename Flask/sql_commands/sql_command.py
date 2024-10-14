import sqlite3

def create_bme680_table():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('databases/data.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS air_quality (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            temperature REAL,
            pressure REAL,
            humidity REAL,
            gas_resistance REAL,
            air_quality_info TEXT,
            battery_level REAL
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_bme680_table()
    print("Table 'bme680' created successfully.")