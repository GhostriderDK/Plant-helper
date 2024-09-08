import network
import time
import ping

# WiFi configuration
SSID = 'Your_SSID'
PASSWORD = 'Your_Password'

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(ssid, password)
        max_attempts = 10
        attempt = 0
        while not wlan.isconnected() and attempt < max_attempts:
            attempt += 1
            print(f"Attempt {attempt}")
            time.sleep(1)
        if not wlan.isconnected():
            print("Could not connect to WiFi")
            return False
    print("Connected to WiFi")
    print("IP Address:", wlan.ifconfig()[0])
    return True

def ping_host(host):
    """
    Ping a host and return True if it is reachable, False otherwise.
    """
    response = ping.ping(host)
    return response is not None

if __name__ == "__main__":
    if connect_wifi(SSID, PASSWORD):
        ip_address = "192.168.1.1"  # Replace with the IP address you want to ping
        if ping_host(ip_address):
            print(f"{ip_address} is reachable")
        else:
            print(f"{ip_address} is not reachable")