import base64
from io import BytesIO
from matplotlib.figure import Figure
from get_data import *
from matplotlib import pyplot as plt
import numpy as np

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

        ax.axhspan(70, 80, facecolor='blue', alpha=0.3)
        ax.axhspan(35, 70, facecolor='green', alpha=0.3)
        ax.axhspan(20, 35, facecolor='red', alpha=0.3)
        
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
        timestamps, soil, time, inf = get_peperomia_data(1)
        avg_soil = sum(soil) / len(soil)
        
        avg_soil = round(avg_soil, 0)
        
        return avg_soil
    except Exception as ex:
        print(ex)
        return "N/A" 

def peperomia_watering(data_points=5000):
    try:
        timestamps, soil, time, info = get_peperomia_data(data_points)
        increase_threshold = 10  # Define the threshold for increase
        last_watering_timestamp = None  # Initialize to store the last detected watering timestamp

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

def air_quality_data(datapoints, num_ticks):
    try:
        temp, humidity, pressure, altitude, gas, gas_info, datetimes = get_air_quality_data(datapoints)
    
        fig = Figure(figsize=(16, 4))  # Set the figure size for a single row of plots
        axs = fig.subplots(1, 4)  # Create a 1x4 grid of subplots

        fig.subplots_adjust(wspace=0.4, bottom=0.4)  # Adjust spacing between plots and bottom margin
        
        # Plot temperature
        axs[0].plot(datetimes, temp, linestyle="solid", c="#11f", linewidth="1.5")
        axs[0].set_title("Temperature")
        axs[0].set_xlabel("Timestamps")
        axs[0].set_ylabel("Temperature (°C)")
        axs[0].tick_params(axis="x", rotation=45, colors="black")  # Rotate x-axis labels for readability
        axs[0].tick_params(axis="y", colors="blue")
        axs[0].spines["left"].set_color("blue")
        axs[0].grid(axis='y', linestyle='--')

        # Plot humidity
        axs[1].plot(datetimes, humidity, linestyle="solid", c="#1f7", linewidth="1.5")
        axs[1].set_title("Humidity")
        axs[1].set_xlabel("Timestamps")
        axs[1].set_ylabel("Humidity (%)")
        axs[1].tick_params(axis="x", rotation=45, colors="black")  # Rotate x-axis labels for readability
        axs[1].tick_params(axis="y", colors="green")
        axs[1].spines["left"].set_color("green")
        axs[1].grid(axis='y', linestyle='--')

        # Plot pressure
        axs[2].plot(datetimes, pressure, linestyle="solid", c="#f11", linewidth="1.5")
        axs[2].set_title("Pressure")
        axs[2].set_xlabel("Timestamps")
        axs[2].set_ylabel("Pressure (hPa)")
        axs[2].tick_params(axis="x", rotation=45, colors="black")  # Rotate x-axis labels for readability
        axs[2].tick_params(axis="y", colors="red")
        axs[2].spines["left"].set_color("red")
        axs[2].grid(axis='y', linestyle='--')

        # Plot gas
        axs[3].plot(datetimes, gas, linestyle="solid", c="#f7a", linewidth="1.5")
        axs[3].set_title("Gas Resistance")
        axs[3].set_xlabel("Timestamps")
        axs[3].set_ylabel("IAQ Value")
        axs[3].tick_params(axis="x", rotation=45, colors="black")  # Rotate x-axis labels for readability
        axs[3].tick_params(axis="y", colors="purple")
        axs[3].spines["left"].set_color("purple")
        axs[3].grid(axis='y', linestyle='--')

        # Set x-ticks for all subplots
        num_ticks = min(num_ticks, len(datetimes))
        tick_positions = range(0, len(datetimes), max(1, len(datetimes) // num_ticks))
        for ax in axs.flat:
            ax.set_xticks(tick_positions)
            ax.set_xticklabels([datetimes[i] for i in tick_positions], rotation=90)  # Rotate and align labels

        fig.patch.set_facecolor("white")
        
        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data
    except Exception as ex:
        print(ex)
        return None

def current_data():
    try:
        # Fetch the latest data
        temp, humidity, pressure, altitude, gas, gas_info, datetimes = get_air_quality_data(1)

        # Define gauge parameters
        gauge_ranges = {
            "Temperature": (0, 50),
            "Humidity": (0, 100),
            "Pressure": (950, 1050),
            "Gas Resistance": (0, 500)
        }
        gauge_values = [temp[0], humidity[0], pressure[0], gas[0]]
        gauge_colors = ["#11f", "#1f7", "#f11", "#f7a"]

        fig = plt.figure(figsize=(16, 4))
        axs = [fig.add_subplot(1, 4, i + 1, projection='polar') for i in range(4)]
        fig.subplots_adjust(hspace=0.5, wspace=0.5)

        for i, (title, (min_val, max_val)) in enumerate(gauge_ranges.items()):
            ax = axs[i]  # Access subplot directly from the list
            value = gauge_values[i]
            color = gauge_colors[i]

            # Normalize value to angle (flip direction: highest value on the right, lowest on the left)
            angle = (1 - (value - min_val) / (max_val - min_val)) * np.pi  # Scale to half-circle, reversed

            # Draw gauge
            ax.bar(angle, 1, color=color, width=0.05)
            ax.set_ylim(0, 1)
            ax.set_title(title, va='bottom')
            ax.set_xticks([])
            ax.set_yticks([])

            # Add numbers to the gauge (only in upper half, flipped)
            for tick in range(min_val, max_val + 1, (max_val - min_val) // 5):
                tick_angle = (1 - (tick - min_val) / (max_val - min_val)) * np.pi  # Scale to half-circle, reversed

                # Place numbers at the calculated angle
                ax.text(tick_angle, 1.1, str(tick), ha='center', va='center', fontsize=8)

                ax.plot([tick_angle, tick_angle], [1.0, 0.95], color='black', linewidth=1)

            # Add true value below the gauge
            ax.text(np.pi, 0.5, f"Value: {value:.1f}", ha='center', va='top', fontsize=10, color='black')

        fig.patch.set_facecolor("white")

        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data
    except Exception as ex:
        print(ex)
        return None