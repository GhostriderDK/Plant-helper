import base64
from io import BytesIO
import matplotlib.pyplot as plt
from flask import Flask, render_template
from matplotlib.figure import Figure
from get_data import *

app = Flask(__name__)
app.run(debug=True)

datapoints = 1000

def neon_data():
    temp, soil, info = get_neon_pothos_data(datapoints)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/moisture-graph')
def moisture_graph():
    # Generate some sample moisture data
    days = np.arange(1, 11)
    moisture_levels = np.random.randint(0, 100, size=10)

    # Create the graph using Figure module
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot(days, moisture_levels)
    ax.set_xlabel('Day')
    ax.set_ylabel('Moisture Level')
    ax.set_title('Moisture Data')
    
    # Save the graph to a BytesIO object
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the graph image as base64
    # image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Render the template with the graph image
    
    return render_template('moisture_graph.html')
    # return render_template('moisture_graph.html', image_base64=image_base64)