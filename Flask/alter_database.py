import sqlite3
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def table_exists(cursor, table_name):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None

def add_auto_increment_column():
    try:
        conn = sqlite3.connect("databases/data.db")
        cur = conn.cursor()
        
        # Drop new peperomia table if it exists
        if table_exists(cur, "peperomia_new"):
            cur.execute("DROP TABLE peperomia_new")
            logger.info("Dropped existing peperomia_new table")
        
        # Create new peperomia table with id column
        cur.execute("""
            CREATE TABLE peperomia_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT,
                soil REAL,
                timestamp TEXT,
                info TEXT
            )
        """)
        logger.info("Created new peperomia table with id column successfully")
        
        # Copy data from old peperomia table to new peperomia table if it exists
        if table_exists(cur, "peperomia"):
            cur.execute("""
                INSERT INTO peperomia_new (datetime, soil, timestamp, info)
                SELECT datetime, soil, timestamp, info FROM peperomia
            """)
            logger.info("Copied data to new peperomia table successfully")
            
            # Drop old peperomia table
            cur.execute("DROP TABLE peperomia")
            logger.info("Dropped old peperomia table successfully")
        
        # Rename new peperomia table to old peperomia table name
        cur.execute("ALTER TABLE peperomia_new RENAME TO peperomia")
        logger.info("Renamed new peperomia table to old table name successfully")
        
        # Drop new neonpothos table if it exists
        if table_exists(cur, "neonpothos_new"):
            cur.execute("DROP TABLE neonpothos_new")
            logger.info("Dropped existing neonpothos_new table")
        
        # Create new neonpothos table with id column
        cur.execute("""
            CREATE TABLE neonpothos_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT,
                temperature REAL,
                soil REAL,
                info TEXT
            )
        """)
        logger.info("Created new neonpothos table with id column successfully")
        
        # Copy data from old neonpothos table to new neonpothos table if it exists
        if table_exists(cur, "neonpothos"):
            cur.execute("""
                INSERT INTO neonpothos_new (datetime, temperature, soil, info)
                SELECT datetime, temperature, soil, info FROM neonpothos
            """)
            logger.info("Copied data to new neonpothos table successfully")
            
            # Drop old neonpothos table
            cur.execute("DROP TABLE neonpothos")
            logger.info("Dropped old neonpothos table successfully")
        
        # Rename new neonpothos table to old neonpothos table name
        cur.execute("ALTER TABLE neonpothos_new RENAME TO neonpothos")
        logger.info("Renamed new neonpothos table to old table name successfully")
        
        conn.commit()
                    
    except sqlite3.Error as sql_e:
        logger.error(f"sqlite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        logger.error(f"Another error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Call the function to add the auto-increment columns
add_auto_increment_column()