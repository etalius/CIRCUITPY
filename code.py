


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

    print("current flight id: ", str(flight_id))
    print("old flight id: ", str(old_flight_id))

    # Case 1: We found a flight that is different than the flight before
    # or we did not have an old flight but we found one now!
    if False and flight_id and (old_flight_id == "XXXX"  or flight_id != old_flight_id):
        w.feed()
        is_showing_time = False
        gc.collect()
        flights.get_flight_details(flight_id, requests)
        old_flight_id = flight_id
        w.feed()
        gc.collect()
        if flights.parse_details_json():
            w.feed()
            gc.collect()
            text.print_label_contents()
            planeG = plane.make_plane()
            w.feed()
            plane_animation(planeG)
            w.feed()
    
            label1, label2, label3 = text.make_text_labels(display)
            ## TODO: update this to use the logos for the planes 
            logoG = plane.make_plane_for_logo()
            # if "united" in constants.airline_name.lower().strip():
            #     logoG = airline_logos.get_logo_g(airline_logos.UNITED, airline_logos.UNITED_COLORS )
            # elif "delta" in constants.airline_name.lower().strip():
            #     logoG = airline_logos.get_logo_g(airline_logos.DELTA, airline_logos.DELTA_COLORS)
            # else:
            #     logoG = plane.make_plane_for_logo()
        
            logoG.append(label1)
            logoG.append(label2)
            logoG.append(label3)
            display.root_group = logoG
            
            w.feed()
            time.sleep(5)
            label3.x=matrixportal.display.width+1
            label3.text=constants.label2_long
            w.feed()
            scroll(label3)
            w.feed()
            label3.text=constants.label2_short
            bbx, bby, bbwidth, bbh = label3.bounding_box
            label3.x=round(display.width / 2 - bbwidth / 2)

        for i in range(5):
            w.feed()
            time.sleep(5)
            gc.collect()
    
    # Case 2: We found the same flight as before, so just keep displaying it for now
    elif False and old_flight_id != "XXXX" and flight_id == old_flight_id:
        w.feed()
        for i in range(5):
            w.feed()
            time.sleep(5)
            gc.collect()
    
    # Case 3: we did not find a new flight and we didn't have one! 
    else:
        w.feed()
        old_flight_id = "XXXX"
        # def update_time(hours=None, minutes=None):
        #     if hours >= 18 or hours < 6:  # evening hours to morning
        #         clock_label.color = color[2]
        #     else:
        #         clock_label.color = color[3]  # daylight hours
        #     if hours > 12:  # Handle times later than 12:59
        #         hours -= 12
        #     elif not hours:  # Handle times between 0:00 and 0:59
        #         hours = 12
        
        #     colon = ":"
        
        #     clock_label.text = "{hours}{colon}{minutes:02d}".format(
        #         hours=hours, minutes=minutes, colon=colon
        #     )
        #     bbx, bby, bbwidth, bbh = clock_label.bounding_box
        #     # Center the label
        #     clock_label.x = round(display.width / 2 - bbwidth / 2)
        #     clock_label.y = display.height // 2
            
        print("Making request to update RTC")
        my_rtc = flights.new_get_time(matrixportal, requests, my_rtc)
        current_time = my_rtc.datetime
        hours = current_time.tm_hour
        minutes = current_time.tm_min
        clock.update_time(hours, minutes, display)
    
        # # check if we need to update the time  - only if the minutes change
        # if is_showing_time:
        #     old_mins = minutes
        #     current_time = my_rtc.datetime
        #     minutes = current_time.tm_min
        
        # if not is_showing_time or minutes != old_mins: 
        #     current_time = my_rtc.datetime
        #     hours = current_time.tm_hour
        #     minutes = current_time.tm_min

        #     clock.update_time(hours, minutes, display)
            
            # group = displayio.Group()  # Create a Group
            # bitmap = displayio.Bitmap(64, 32, 2)  # Create a bitmap object,width, height, bit depth
            # color = displayio.Palette(4)  # Create a color palette
            # color[0] = 0x000000  # black background
            # color[1] = 0x111184  # dark blue
            # color[2] = 0xFED1DA  # light pink for day 
            # color[3] = 0x85FF00  # greenish
            
            # # Create a TileGrid using the Bitmap and Palette
            # tile_grid = displayio.TileGrid(bitmap, pixel_shader=color)
            # group.append(tile_grid)  # Add the TileGrid to the Group
            # display.root_group = group
            # clock_font = bitmap_font.load_font("IBMPlexMono-Medium-24_jep.bdf")
            # clock_label = Label(clock_font)

            # update_time(hours, minutes, display)  # Display whatever time is on the board
            # group.append(clock_label)  # add the clock label to the group
        w.feed()
        is_showing_time = True
        for i in range(20):
            w.feed()
            current_time = my_rtc.datetime
            hours = current_time.tm_hour
            minutes = current_time.tm_min
            clock.update_time(hours, minutes, display)
            time.sleep(5)
            gc.collect()
 

    