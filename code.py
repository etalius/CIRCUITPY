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
esp, wifi = internet.setup_internet()
internet.check_connection(esp, wifi)

# Make matrix portal
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL,
                            debug=True,
                            esp=esp,
                            headers=constants.rheaders)
display = matrixportal.display
w.feed()

# Init the clock
my_rtc = rtc.RTC()
my_rtc = flights.new_get_time(matrixportal, wifi, my_rtc)

weather.ensure(wifi)
now = my_rtc.datetime
weather.show(display, now.tm_hour, now.tm_min)
for i in range(4):
    w.feed()
    time.sleep(5)

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
fail_streak = 0
idle_weather = True

while True:
    internet.check_connection(esp, wifi)
    w.feed()
    response = flights.get_flights(matrixportal, wifi)
    w.feed()

    if response is False:
        fail_streak += 1
        flight_id = None
        local_time = None
        print("Flight lookup failed, streak", fail_streak)
        if fail_streak >= 3:
            internet.recover_network(wifi)
            fail_streak = 0
    elif not response:
        fail_streak = 0
        flight_id = None
        local_time = None
    else:
        fail_streak = 0
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
        if flights.get_flight_details(flight_id, wifi):
            flights.parse_details_json()
        old_flight_id = flight_id
        w.feed()
        gc.collect()
        text.print_label_contents()
        gc.collect()
        planeG = plane.make_plane()
        elev = constants.plane_elev_deg
        if elev < 0:
            elev = 0
        if elev > 40:
            elev = 40
        planeG.y = 14 - int(elev / 40 * 10)
        w.feed()
        plane_animation(planeG)
        w.feed()
        gc.collect()

        label1, label2, label3 = text.make_text_labels(display)
        airline = constants.airline_name.lower().strip()

        if "united" in airline:
            logoG = airline_logos.get_logo_g(airline_logos.UNITED, airline_logos.UNITED_COLORS )
        elif "delta" in airline:
            logoG = airline_logos.get_logo_g(airline_logos.DELTA, airline_logos.DELTA_COLORS)
        elif 'lufthansa' in airline:
            logoG = airline_logos.get_logo_g(airline_logos.LUTHANSA, airline_logos.LUTHANSA_COLORS)
        elif 'british' in airline:
            logoG = airline_logos.get_logo_g(airline_logos.BRITISH, airline_logos.BRITISH_COLORS)
        elif "canada" in airline:
            logoG = airline_logos.get_logo_g(airline_logos.AIR_CANADA, airline_logos.AIR_CANADA_COLORS)
        elif 'southwest' in airline:
            logoG = airline_logos.get_logo_g(airline_logos.SOUTHWEST, airline_logos.SOUTHWEST_COLORS)
        elif 'alaska' in airline:
            logoG = airline_logos.get_logo_g(airline_logos.ALAKSA, airline_logos.ALASKA_COLORS)
        elif "american" in airline:
            logoG = airline_logos.get_logo_g(airline_logos.AMERICAN, airline_logos.AMERICAN_COLORS)
        elif "spirit" in airline:
            logoG = airline_logos.get_logo_g(airline_logos.SPIRIT, airline_logos.SPIRIT_COLORS)
        else:
            logoG = plane.make_plane_for_logo()

        logoG.append(label1)
        logoG.append(label2)
        logoG.append(label3)
        logoG.append(text.make_position_marker(display))
        display.root_group = logoG
        gc.collect()

        w.feed()
        time.sleep(5)
        if constants.label2_short and "-" in constants.label2_short and constants.label2_long:
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
    
    # Case 3: no flight — alternate weather and the clock
    else:
        w.feed()
        old_flight_id = "XXXX"
        gc.collect()

        if idle_weather:
            is_showing_time = False
            weather.ensure(wifi)
            current_time = my_rtc.datetime
            weather.show(display, current_time.tm_hour, current_time.tm_min)
            idle_weather = False
            gc.collect()
            w.feed()
            for i in range(5):
                w.feed()
                time.sleep(5)
                gc.collect()
        else:
            is_showing_time = True
            print("Making request to update RTC")
            my_rtc = flights.new_get_time(matrixportal, wifi, my_rtc)
            current_time = my_rtc.datetime
            clock.update_time(current_time.tm_hour, current_time.tm_min, display)
            idle_weather = True
            gc.collect()
            w.feed()
            for i in range(5):
                w.feed()
                current_time = my_rtc.datetime
                clock.update_time(current_time.tm_hour, current_time.tm_min, display)
                time.sleep(5)
                gc.collect()
 

    