import base64
from io import BytesIO
from flask import Flask, render_template
from matplotlib.figure import Figure
from get_data import *

app = Flask(__name__)
app.run(debug=True)

datapoints = 1000

def neon_data():
    timestamps, temp, soil, info = get_neon_pothos_data(datapoints)
   
    fig = Figure() 
    ax = fig.add_subplot(1, 1)
    fig.subplots_adjust(bottom=0.1)
    ax.set_facecolor("white")
    ax.plot(timestamps, soil, linestyle="solid", c="#11f", linewidth="1.5")
    ax.set_ylabel("moisture in %")
    ax.tick_params(axis="y", colors="blue")
    ax.spines["left"].set_color("blue")
    tick_positions = range(0, len(timestamps), len(timestamps) // num_ticks)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([])
    ax.grid(axis='y', linestyle='--')
    ax.set_title("Neon Pothos Moisture Level", fontsize=15)
    
    fig.subplots_adjust(bottom=0.3)
    fig.patch.set_facecolor("orange")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/moisture-graph')
def moisture_graph():
    neonpothos_data = neon_data()
    return render_template('moisture_graph.html', neonpothos_data=neonpothos_data)
    # return render_template('moisture_graph.html', image_base64=image_base64)