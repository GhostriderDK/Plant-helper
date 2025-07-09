from flask import Flask, render_template, request, jsonify     
import backend as bk

app = Flask(__name__)


datapoints = 2000
num_ticks = 10

last_log = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/overview')
def overview():
    try:
        global last_log

        peperomia_level = bk.get_peperomia_level()
        if peperomia_level == "Wet":
            peperomia_class = "wet"
        elif peperomia_level == "Moist":
            peperomia_class = "moist"
        elif peperomia_level == "Dry":
            peperomia_class = "dry"
        
        avg_peperomia = bk.get_current_pct_peperomia()
        
        watering_timestamp = bk.peperomia_watering()
        if watering_timestamp != None:
            last_water_peperomia = watering_timestamp
            last_log = watering_timestamp
        else:
            last_water_peperomia = last_log
            
        neonpothos_level = bk.get_neonpothos_level()
        if neonpothos_level == "Wet":
            neonpothos_class = "wet"
        elif neonpothos_level == "Moist":
            neonpothos_class = "moist"
        elif neonpothos_level == "Dry":
            neonpothos_class = "dry"
    except Exception as ex:
        print(ex)
        peperomia_level = "N/A"
        peperomia_class = "wet"
        avg_peperomia = "N/A"
        last_water_peperomia = "N/A"
        neonpothos_level = "N/A"
        neonpothos_class = "wet"    
    finally:
        return render_template('overview.html', peperomia_level=peperomia_level, neonpothos_level=neonpothos_level,
                            peperomia_class=peperomia_class, neonpothos_class=neonpothos_class, avg_peperomia=avg_peperomia, last_water_peperomia=last_water_peperomia)

@app.route('/moisture-graph')
def moisture_graph():
    try:
        peperomia_graph = bk.peperomia_data(6000, num_ticks)
    except Exception as ex:
        print(ex)
        peperomia_graph = None
    finally:    
        return render_template('moisture_graph.html', peperomia_graph=peperomia_graph)
    # return render_template('moisture_graph.html', image_base64=image_base64)

@app.route('/overview-graph')
def overview_graph():
    try:
        peperomia_graph = bk.peperomia_data(datapoints, num_ticks)
        global last_log

        peperomia_level = bk.get_peperomia_level()
        if peperomia_level == "Wet":
            peperomia_class = "wet"
        elif peperomia_level == "Moist":
            peperomia_class = "moist"
        elif peperomia_level == "Dry":
            peperomia_class = "dry"
        
        avg_peperomia = bk.get_current_pct_peperomia()
        
        watering_timestamp = bk.peperomia_watering()
        if watering_timestamp != None:
            last_water_peperomia = watering_timestamp
            last_log = watering_timestamp
        else:
            last_water_peperomia = last_log
            
        neonpothos_level = bk.get_neonpothos_level()
        if neonpothos_level == "Wet":
            neonpothos_class = "wet"
        elif neonpothos_level == "Moist":
            neonpothos_class = "moist"
        elif neonpothos_level == "Dry":
            neonpothos_class = "dry"
    except Exception as ex:
        print(ex)
        peperomia_graph = None
        peperomia_level = "N/A"
        peperomia_class = "wet"
        avg_peperomia = "N/A"
        last_water_peperomia = "N/A"
        neonpothos_level = "N/A"
        neonpothos_class = "wet"
    finally:
        return render_template('overview_graph.html', peperomia_graph=peperomia_graph, peperomia_level=peperomia_level, neonpothos_level=neonpothos_level,
                            peperomia_class=peperomia_class, neonpothos_class=neonpothos_class, avg_peperomia=avg_peperomia, last_water_peperomia=last_water_peperomia)

@app.route('/plant-bot')
def plant_bot():
    return render_template('bot.html')

@app.route('/air-sensor')
def air_sensor():
    try:
        air_quality_graph = bk.air_quality_data(6000, num_ticks)
        current_data_gauges = bk.current_data()
    except Exception as ex:
        print(ex)
        air_quality_graph = None
        current_data_gauges = None
    finally:    
        return render_template('air_sensor.html', air_quality_graph=air_quality_graph, current_data_gauges=current_data_gauges)


@app.route('/bot-post', methods=['POST'])
def bot_post():
    pass
# plantbot here

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

