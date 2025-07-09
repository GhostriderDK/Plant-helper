import sqlite3

def delete_air_quality_table():
    conn = sqlite3.connect('databases/data.db')
    cursor = conn.cursor()

    # Drop the Air_quality table if it exists
    cursor.execute('''
        DROP TABLE IF EXISTS Air_quality
    ''')

    conn.commit()
    conn.close()

delete_air_quality_table()

def create_bme680_table():
    conn = sqlite3.connect('databases/data.db')
    cursor = conn.cursor()

    # Create a table for BME680 data if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Air_quality (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            pressure REAL NOT NULL,
            altitude REAL NOT NULL,
            gas_resistance REAL NOT NULL,
            gas_info TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def create_delete_log_and_trigger():
    conn = sqlite3.connect('databases/data.db')
    cursor = conn.cursor()

    # Create the delete_log table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS delete_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            deleted_id INTEGER,
            deleted_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the trigger for logging deletions from Air_quality
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS log_air_quality_deletes
        AFTER DELETE ON Air_quality
        BEGIN
            INSERT INTO delete_log (deleted_id) VALUES (OLD.id);
        END;
    ''')

    conn.commit()
    conn.close()

create_bme680_table()
#create_delete_log_and_trigger()
