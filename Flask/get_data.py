import sqlite3


def get_neon_pothos_data(number_of_rows):
    while True:
        query = """SELECT * FROM neonpothos ORDER BY id DESC;"""
        datetimes = []
        moisture_level = []
        timestamp = []
        level = []
        try:
            conn = sqlite3.connect("databases/data.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                datetimes.append(row[1])
                moisture_level.append(row[2])
                timestamp.append(row[3]) 
                level.append(row[4]) 
            return datetimes, moisture_level, timestamp, level          
        except sqlite3.Error as sql_e:
            print(f"sqlite error occurred: {sql_e}")
            conn.rollback()

        except Exception as e:
            print(f"Another error occured: {e}")
        finally:
            conn.close()
get_neon_pothos_data(10)

def get_peperomia_data(number_of_rows):
    while True:
        query = """SELECT * FROM peperomia ORDER BY id DESC;"""
        datetimes = []
        moisture_level = []
        timestamp = []
        level = []
        try:
            conn = sqlite3.connect("databases/data.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                datetimes.append(row[1])
                moisture_level.append(row[2])
                timestamp.append(row[3]) 
                level.append(row[4])
            return datetimes, moisture_level, timestamp, level          
        except sqlite3.Error as sql_e:
            print(f"sqlite error occurred: {sql_e}")
            conn.rollback()

        except Exception as e:
            print(f"Another error occured: {e}")
        finally:
            conn.close()
get_peperomia_data(10)


################## Smart Home Automation ##################


def get_air_quality_data(number_of_rows):
    while True:
        query = """SELECT * FROM air_quality ORDER BY id DESC;"""
        datetimes = []
        temperature = []
        pressure = []
        humidity = []
        gas = []
        battery = []
        try:
            conn = sqlite3.connect("databases/data.db")
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchmany(number_of_rows)
            for row in reversed(rows):
                datetimes.append(row[0])
                temperature.append(row[1])
                pressure.append(row[2])
                humidity.append(row[3])
                gas.append(row[4])
                battery.append(row[5]) 
            return datetimes, temperature, pressure, humidity, gas, battery          
        except sqlite3.Error as sql_e:
            print(f"sqlite error occurred: {sql_e}")
            conn.rollback()

        except Exception as e:
            print(f"Another error occured: {e}")
        finally:
            conn.close()