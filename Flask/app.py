from flask import Flask, render_template
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
    level = bk.get_peperomia_level()
    if level == "Wet":
        system_status_class = "Wet"
    elif level == "Moist":
        system_status_class = "Moist"
    elif level == "Dry":
        system_status_class = "Dry"
    return render_template('overview.html', level=level, system_status_class=system_status_class)

@app.route('/moisture-graph')
def moisture_graph():
    peperomia_graph = bk.peperomia_data(datapoints, num_ticks)
    return render_template('moisture_graph.html', peperomia_graph=peperomia_graph)
    # return render_template('moisture_graph.html', image_base64=image_base64)