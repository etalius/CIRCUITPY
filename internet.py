
import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from microcontroller import watchdog as w
import neopixel
from digitalio import DigitalInOut
import adafruit_connection_manager
import adafruit_requests
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi.adafruit_esp32spi_wifimanager import WiFiManager
import busio
import os
import constants

import displayio

def setup_internet():
    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    pool = adafruit_connection_manager.get_radio_socketpool(esp)
    ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
    # requests = adafruit_requests.Session(pool, ssl_context)
    ssid = os.getenv("CIRCUITPY_WIFI_SSID")
    password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
    wifi = WiFiManager(esp, ssid, password)
    return esp, wifi

def connect_to_wifi(esp):
    # ssid = os.getenv("CIRCUITPY_WIFI_SSID")
    # password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
    # print("in connect to wifi")
    # while not esp.is_connected:
    #     try:
    #         esp.connect_AP(ssid, password)
    #     except OSError as e:
    #         print("could not connect to AP, retrying: ", e)
    #         continue
    return esp

def check_connection(esp):
    print("Check and reconnect WiFi")
    attempts=10
    attempt=1
    while (not esp.is_connected) and attempt<attempts:
        try:
            print("tying to connect!")
            connect_to_wifi(esp)
        except OSError as e:
            print(e.__class__.__name__+"--------------------------------------")
            print(e)
        attempt+=1
    if esp.is_connected:
        print("Successfully connected.")
    else:
        print("Failed to connect.")
        time.sleep(17) #sleep for 17 seconds so that watchdog resets the board