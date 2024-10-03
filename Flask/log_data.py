import sqlite3
from datetime import datetime
import json
import paho.mqtt.subscribe as subscribe

print("subscribe mqtt script running")


def peperomia_message(client, userdata, message):
    query = """INSERT INTO peperomia (datetime, soil, timestamp, info) VALUES(?, ?, ?, ?)"""
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")
    peperomia_data = json.loads(message.payload.decode())
    data = (now, peperomia_data['soil'], peperomia_data['timestamp'], peperomia_data['level'])

    try:
        conn = sqlite3.connect("databases/data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
                    
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Another error occured: {e}")
    finally:
        conn.close()
        #delete_peperomia_data()

def delete_peperomia_data():
    try:
        conn = sqlite3.connect("databases/data.db")
        cur = conn.cursor()
        
        # Delete data points except the 5000 newest
        cur.execute("""
            DELETE FROM peperomia
            WHERE id NOT IN (
                SELECT id
                FROM peperomia
                ORDER BY id DESC
                LIMIT 5000
            )
        """)
        
        conn.commit()
                    
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Another error occurred: {e}")
    finally:
        conn.close()

def neon_pothos_message(client, userdata, message):
    query = """INSERT INTO peperomia (datetime, temperature, soil, info) VALUES(?, ?, ?, ?)"""
    now = datetime.now()
    now = now.strftime("%d/%m/%y %H:%M:%S")
    neon_pothos_data = json.loads(message.payload.decode())
    data = (now, neon_pothos_data['soil'], neon_pothos_data['timestamp'], neon_pothos_data['level'])
    
    try:
        conn = sqlite3.connect("databases/data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
                    
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Another error occured: {e}")
    finally:
        conn.close()
        #delete_neon_pothos_data()

def delete_neon_pothos_data():
    try:
        conn = sqlite3.connect("databases/data.db")
        cur = conn.cursor()
        
        # Delete data points except the 5000 newest
        cur.execute("""
            DELETE FROM neonpothos
            WHERE id NOT IN (
                SELECT id
                FROM neonpothos
                ORDER BY id DESC
                LIMIT 5000
            )
        """)
        
        conn.commit()
                    
    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        conn.rollback()

    except Exception as e:
        print(f"Another error occurred: {e}")
    finally:
        conn.close()


topic_function_map = {
    "plant/pothos/json": neon_pothos_message,
    "plant/peperomia/json": peperomia_message,
}


def on_message_received(client, userdata, message):
    topic = message.topic
    if topic in topic_function_map:
        topic_function_map[topic](client, userdata, message)
    else:
        print(f"No function mapped for topic: {topic}")

topics = ["plant/pothos/json", "plant/peperomia/json"]
subscribe.callback(on_message_received, topics, hostname="localhost", userdata={"message_count": 0})