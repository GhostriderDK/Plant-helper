from flask import Flask, render_template, url_for, request, redirect    
import backend as bk

app = Flask(__name__)


datapoints = 20000
num_ticks = 10

last_log = None

@app.route('/')
def home():
    return render_template('plant_home.html')

################## Plant monitoring ##################

@app.route('/overview')
def overview():
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
    return render_template('overview.html', peperomia_level=peperomia_level, neonpothos_level=neonpothos_level,
                            peperomia_class=peperomia_class, neonpothos_class=neonpothos_class, avg_peperomia=avg_peperomia, last_water_peperomia=last_water_peperomia)

@app.route('/moisture-graph')
def moisture_graph():
    peperomia_graph = bk.peperomia_data(datapoints, num_ticks)
    return render_template('moisture_graph.html', peperomia_graph=peperomia_graph)

@app.route('/overview-plant')
def overview_graph():
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
    return render_template('overview-graph.html', peperomia_graph=peperomia_graph, peperomia_level=peperomia_level, neonpothos_level=neonpothos_level,
                            peperomia_class=peperomia_class, neonpothos_class=neonpothos_class, avg_peperomia=avg_peperomia, last_water_peperomia=last_water_peperomia)


################## Smart home automation ##################

@app.route('/smart-home')
def smart_home():
    return render_template('smarthome_home.html')

@app.route('/device-control')
def devices():
    return render_template('smarthome_devices.html')

@app.route('/settings')
def settings():
    return render_template('smarthome_settings.html')

@app.route('/air-quality-overview')
def air_quality_overview():
    air_quality_graph = bk.get_air_data(datapoints, num_ticks)
    return render_template('air_quality_overview.html', air_quality_graph=air_quality_graph)


################## flask run ##################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

