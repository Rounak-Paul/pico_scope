import network
import time

class WIFI:
    def __init__(self,ssid, password):
        self.SSID = ssid
        self.PASS = password
    
    def connect(self):
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        available_networks = wifi.scan()
        #print(available_networks)
        wifi.connect(self.SSID, self.PASS)

        while not wifi.isconnected():
            print("Waiting for connection ...")
            time.sleep(1)

        return wifi.ifconfig()

