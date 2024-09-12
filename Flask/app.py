from flask import Flask, render_template, url_for, request, redirect    
import backend as bk

app = Flask(__name__)
app.run(debug=True)

datapoints = 20000
num_ticks = 10

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/overview')
def overview():
    peperomia_level = bk.get_peperomia_level()
    if peperomia_level == "Wet":
        peperomia_class = "wet"
    elif peperomia_level == "Moist":
        peperomia_class = "moist"
    elif peperomia_level == "Dry":
        peperomia_class = "dry"

    neonpothos_level = bk.get_neonpothos_level()
    if neonpothos_level == "Wet":
        neonpothos_class = "wet"
    elif neonpothos_level == "Moist":
        neonpothos_class = "moist"
    elif neonpothos_level == "Dry":
        neonpothos_class = "dry"
    return render_template('overview.html', peperomia_level=peperomia_level, neonpothos_level=neonpothos_level, peperomia_class=peperomia_class, neonpothos_class=neonpothos_class)

@app.route('/moisture-graph')
def moisture_graph():
    peperomia_graph = bk.peperomia_data(datapoints, num_ticks)
    return render_template('moisture_graph.html', peperomia_graph=peperomia_graph)
    # return render_template('moisture_graph.html', image_base64=image_base64)