import network
import time

SSID = "your SSID"
PASSWORD = "your Password"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Station mode
    wlan.active(True)  # Enable WiFi
    wlan.connect(SSID, PASSWORD)

    print("Connecting to WiFi...", end="")
    for _ in range(10):  # Wait up to 10 seconds
        if wlan.isconnected():
            print("\nConnected!")
            print("IP Address:", wlan.ifconfig()[0])
            return wlan.ifconfig()[0]
        print(".", end="")
        time.sleep(1)
    
    print("\nFailed to connect!")
    return None

connect_wifi()
