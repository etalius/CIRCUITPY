import time
from adafruit_matrixportal.matrixportal import MatrixPortal
from adafruit_display_text.label import Label
from microcontroller import watchdog as w
from watchdog import WatchDogMode
import adafruit_requests as requests
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.network import Network
import board
import gc
import displayio
import rtc

import plane
import flights
import constants
import internet
import airline_logos
import text
import clock
import weather

# Watchdog init to handle disconnecting from WiFi
w.timeout=16 # timeout in seconds
w.mode = WatchDogMode.RESET

# Init the globals 
constants.init_globals()

# Set up WiFi and connect
esp, requests = internet.setup_internet()
esp = internet.connect_to_wifi(esp)

# Make matrix portal
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL,
                            debug=True,
                            esp=esp,
                            headers=constants.rheaders)
display = matrixportal.display
w.feed()

# Init the clock
my_rtc = rtc.RTC()
my_rtc = flights.new_get_time(matrixportal, requests, my_rtc)

def plane_animation(planeG):
    display.root_group = planeG
    for i in range(-12,matrixportal.display.width+24, 1):
        planeG.x=i
        w.feed()
        time.sleep(constants.PLANE_SPEED)
        display.root_group = planeG

def scroll(line):
    line.x=matrixportal.display.width
    for i in range(matrixportal.display.width+1, 0-line.bounding_box[2], -1):
        line.x=i
        w.feed()
        time.sleep(constants.TEXT_SPEED)
        
old_flight_id = "XXXX"
is_showing_time = False

while True:
    internet.check_connection(esp)
    w.feed()
    response = flights.get_flights(matrixportal, requests)
    w.feed()
    
    if not response:
        flight_id = None
        local_time = None
    else:
        flight_id, local_time = response
    w.feed()

    # labels = weather.show_weather(display)
    # group = displayio.Group(scale=1, x=0, y=0)
    # for l in labels:
    #     group.append(l)
    # display.root_group = group

    # for i in range(100):
    #     time.sleep(10)
    #     w.feed()


    # Case 1: We found a flight that is different than the flight before
    # or we did not have an old flight but we found one now!
    if (flight_id and (old_flight_id == "XXXX"  or flight_id != old_flight_id)):
        w.feed()
        is_showing_time = False
        old_flight_id = flight_id
        gc.collect()
        flights.get_flight_details(flight_id, requests)
        old_flight_id = flight_id
        w.feed()
        gc.collect()
        if flights.parse_details_json():
            w.feed()
            gc.collect()
            text.print_label_contents()
            gc.collect()
            planeG = plane.make_plane()
            w.feed()
            plane_animation(planeG)
            w.feed()
            gc.collect()
    
            label1, label2, label3 = text.make_text_labels(display)

            if "united" in constants.airline_name.lower().strip():
                logoG = airline_logos.get_logo_g(airline_logos.UNITED, airline_logos.UNITED_COLORS )
            elif "delta" in constants.airline_name.lower().strip():
                logoG = airline_logos.get_logo_g(airline_logos.DELTA, airline_logos.DELTA_COLORS)
            elif 'lufthansa' in constants.airline_name.lower().strip():
                logoG = airline_logos.get_logo_g(airline_logos.LUTHANSA, airline_logos.LUTHANSA_COLORS)
            elif 'british' in constants.airline_name.lower().strip():
                logoG = airline_logos.get_logo_g(airline_logos.BRITISH, airline_logos.BRITISH_COLORS)
            elif "canada" in constants.airline_name.lower().strip():
                logoG = airline_logos.get_logo_g(airline_logos.AIR_CANADA, airline_logos.AIR_CANADA_COLORS)
            elif 'southwest' in constants.airline_name.lower().strip():
                logoG = airline_logos.get_logo_g(airline_logos.SOUTHWEST, airline_logos.SOUTHWEST_COLORS)
            elif 'alaska' in constants.airline_name.lower().strip():
                logoG = airline_logos.get_logo_g(airline_logos.ALAKSA, airline_logos.ALASKA_COLORS)
            else:
                logoG = plane.make_plane_for_logo()
        
            logoG.append(label1)
            logoG.append(label2)
            logoG.append(label3)
            display.root_group = logoG
            gc.collect()
            
            w.feed()
            time.sleep(5)
            label3.x=matrixportal.display.width+1
            label3.text=constants.label2_long
            gc.collect()
            w.feed()
            scroll(label3)
            w.feed()
            label3.text=constants.label2_short
            bbx, bby, bbwidth, bbh = label3.bounding_box
            label3.x=round(display.width / 2 - bbwidth / 2)
            gc.collect()

        for i in range(5):
            w.feed()
            time.sleep(5)
            gc.collect()
    
    # Case 2: We found the same flight as before, so just keep displaying it for now
    elif old_flight_id != "XXXX" and flight_id == old_flight_id:
        w.feed()
        for i in range(5):
            w.feed()
            time.sleep(5)
            gc.collect()
    
    # Case 3: we did not find a new flight and we didn't have one! 
    else:
        w.feed()
        old_flight_id = "XXXX"
        is_showing_time = True
        gc.collect()

        w.feed()
        print("Making request to update RTC")
        my_rtc = flights.new_get_time(matrixportal, requests, my_rtc)
        current_time = my_rtc.datetime
        hours = current_time.tm_hour
        minutes = current_time.tm_min
        clock.update_time(hours, minutes, display)
        gc.collect()
    
        w.feed()
        for i in range(5):
            w.feed()
            current_time = my_rtc.datetime
            hours = current_time.tm_hour
            minutes = current_time.tm_min
            clock.update_time(hours, minutes, display)
            time.sleep(5)
            gc.collect()
 

    