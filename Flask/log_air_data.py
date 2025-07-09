import sqlite3
from datetime import datetime
import json
import paho.mqtt.subscribe as subscribe

print("subscribe mqtt script running")


def air_quality_message(client, userdata, message):
    print(json.loads(message.payload.decode()))
    query = """INSERT INTO Air_quality (temperature, humidity, pressure, altitude, gas_resistance, gas_info, timestamp) VALUES(?, ?, ?, ?, ?, ?, ?)"""
    now = datetime.now().strftime("%d/%m/%y %H:%M")
    air_quality_data = json.loads(message.payload.decode())
    data = (air_quality_data['TEMP'], air_quality_data['HUMIDITY'], air_quality_data['PRESSURE'],
            air_quality_data['ALTITUDE'], air_quality_data['IAQ'], air_quality_data['IAQ_INFO'], now)

    conn = None
    try:
        conn = sqlite3.connect("databases/data.db")
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        # Optional: delete_air_quality_data()

    except sqlite3.Error as sql_e:
        print(f"sqlite error occurred: {sql_e}")
        if conn:
            conn.rollback()

    except Exception as e:
        print(f"Another error occured: {e}")

    finally:
        if conn:
            conn.close()

topic_function_map = {
    "air_quality/roam/json": air_quality_message,
}


def on_message_received(client, userdata, message):
    topic = message.topic
    if topic in topic_function_map:
        topic_function_map[topic](client, userdata, message)
    else:
        print(f"No function mapped for topic: {topic}")

topics = ["air_quality/roam/json"]
subscribe.callback(on_message_received, topics, hostname="localhost", userdata={"message_count": 0})