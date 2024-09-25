import base64
from io import BytesIO
from matplotlib.figure import Figure
from get_data import *

def peperomia_data(datapoints, num_ticks):
    try:
        timestamps, soil, time, info = get_peperomia_data(datapoints)
    
        fig = Figure()
        ax = fig.subplots()
        fig.subplots_adjust(bottom=0.3)
        
        ax.tick_params(axis='x', which='both', rotation=90)
        ax.set_facecolor("white")
        ax.plot(timestamps, soil, linestyle="solid", c="#11f", linewidth="1.5")
        ax.set_xlabel("Timestamps")
        ax.set_ylabel("moisture in %")
        ax.tick_params(axis="x", colors="black")
        ax.tick_params(axis="y", colors="blue")
        ax.spines["left"].set_color("blue")
        ax.grid(axis='y', linestyle='--')
        num_ticks = min(num_ticks, len(timestamps))
        tick_positions = range(0, len(timestamps), max(1, len(timestamps) // num_ticks))
        ax.set_xticks(tick_positions)
        fig.patch.set_facecolor("white")
        
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data
    except Exception as ex:
        print(ex)
        return None

def get_peperomia_level():
    try:
        timestamps, soil, time, info = get_peperomia_data(1)
        
        if info.count(info[0]) == len(info):
            return info[0]
        else:
            pass
    except Exception as ex:
        print(ex)
        return "N/A"
    

def get_current_pct_peperomia():
    try:
        timestamps, soil, time, inf = get_peperomia_data(3)
        avg_soil = sum(soil) / len(soil)
        
        avg_soil = round(avg_soil, 0)
        
        return avg_soil
    except Exception as ex:
        print(ex)
        return "N/A" 

def peperomia_watering(data_points=1000):
    try:
        timestamps, soil, time, info = get_peperomia_data(data_points)
        increase_threshold = 10  
        last_watering_timestamp = None  

        for i in range(1, len(soil)):
            if soil[i] - soil[i - 1] > increase_threshold:
                last_watering_timestamp = timestamps[i]

        return last_watering_timestamp
    except Exception as ex:
        print(ex)
        return "N/A"
    
    

def get_neonpothos_level(timestamps="", soil = 50, time = 1, info = ["Moist", "Moist"]):
    try:
        timestamps, soil, time, inf = get_neon_pothos_data(10)
        
        if info.count(info[0]) == len(info):
            return info[0]
        else:
            pass
    except Exception as ex:
        print(ex)
        return "N/A"