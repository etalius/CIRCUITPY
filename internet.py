
import time
import board
from microcontroller import watchdog as w
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi.adafruit_esp32spi_wifimanager import WiFiManager
import busio
import os


def setup_internet():
    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    ssid = os.getenv("CIRCUITPY_WIFI_SSID")
    password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
    wifi = WiFiManager(esp, ssid, password)
    return esp, wifi


def recover_network(wifi):
    print("Resetting ESP32 and reconnecting WiFi")
    w.feed()
    try:
        wifi.reset()
    except Exception as e:
        print(e.__class__.__name__, e)
    w.feed()
    try:
        wifi.connect()
    except Exception as e:
        print(e.__class__.__name__, e)
    w.feed()


def check_connection(esp, wifi):
    print("Check and reconnect WiFi")
    w.feed()
    if esp.is_connected:
        print("Successfully connected.")
        return True

    attempts = 5
    for attempt in range(1, attempts + 1):
        print("trying to connect!", attempt)
        recover_network(wifi)
        if esp.is_connected:
            print("Successfully connected.")
            return True
        time.sleep(1)
        w.feed()

    print("Failed to connect.")
    time.sleep(17)
    return False


def close_response(response):
    if not response:
        return
    try:
        response.close()
    except Exception:
        pass
