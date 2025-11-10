


from microcontroller import watchdog as w
import constants
from adafruit_portalbase.network import HttpError
import json
from microcontroller import watchdog as w
from watchdog import WatchDogMode
import time

json_size = 14336
json_bytes = bytearray(json_size)



# Helper function to find the nth weekday of a month (e.g., second Sunday in March)
def get_nth_weekday(year, month, weekday, n):
    first_day_of_month = time.struct_time((year, month, 1, 0, 0, 0, 0, 0, 0))
    first_weekday = first_day_of_month.tm_wday  # 0=Monday, 6=Sunday
    day_of_month = (7 * (n - 1)) + (weekday - first_weekday) if weekday >= first_weekday else (7 * (n - 1)) + (7 + weekday - first_weekday)
    return day_of_month

# Check if the given timestamp is in DST
def is_dst(utc_time):
    year = utc_time.tm_year
    second_sunday_march = get_nth_weekday(year, 3, 6, 2)
    first_sunday_november = get_nth_weekday(year, 11, 6, 1)
    start_of_dst = time.struct_time((year, 3, second_sunday_march, 2, 0, 0, 0, 0, 0))  # Second Sunday in March, 2:00 AM
    end_of_dst = time.struct_time((year, 11, first_sunday_november, 2, 0, 0, 0, 0, 0))  # First Sunday in November, 2:00 AM
    start_timestamp = time.mktime(start_of_dst)
    end_timestamp = time.mktime(end_of_dst)
    
    current_timestamp = time.mktime(utc_time)
    return start_timestamp <= current_timestamp < end_timestamp

FLIGHT_LONG_DETAILS_HEAD="https://data-live.flightradar24.com/clickhandler/?flight="

def get_flights(matrixportal, requests):
    matrixportal.url=constants.FLIGHT_SEARCH_URL
    try:
        response_raw=requests.get(url=constants.FLIGHT_SEARCH_URL,headers=constants.rheaders)
        response= response_raw.json()
    except Exception as e:
        print(e.__class__.__name__+"--------------------------------------")
        print(e)
        return False
    print(response)
    if len(response)==3:
        for flight_id, flight_info in response.items():
            # the JSON has three main fields, we want the one that's a flight ID
            if not (flight_id=="version" or flight_id=="full_count"):
                if len(flight_info)>13:
                    print(flight_id)
                    timestamp = flight_info[10]
                    if constants.IS_DST:
                        adjusted_time = time.localtime(timestamp - (7 * 3600))
                    else:
                        adjusted_time = time.localtime(timestamp - (8 * 3600))
                    return flight_id, adjusted_time
    else:
        return None

def new_get_time(matrixportal, requests, my_rtc):
    new_url = 'http://api.timezonedb.com/v2.1/get-time-zone?key=EPWKTIIIXP9B&format=json&by=zone&zone=America/Los_Angeles'
    matrixportal.url = new_url
    try:
        response=requests.get(url=new_url).json()
    except Exception as e:
        print(e.__class__.__name__+"--------------------------------------")
        print(e)
        return my_rtc
    
    time_str = response["formatted"]
    date, time_str = time_str.split(" ")
    year, month, day = [int(x) for x in date.split("-")]
    hour, minute, sec = [int(x) for x in time_str.split(":")]
    is_dst = response['abbreviation'] == 'PDT'
    week_day = 1
    year_day = 1
    
    now = time.struct_time(
        (year, month, day, hour, minute, sec, week_day, year_day, is_dst)
    )
    print(now)
    my_rtc.datetime = now
    print("updated rtc!!")
    
    return my_rtc



def get_time(matrixportal, requests, my_rtc):
    matrixportal.url = "http://worldtimeapi.org/api/ip"
    try:
        response=requests.get(url="http://worldtimeapi.org/api/ip").json()
    except Exception as e:
        print(e.__class__.__name__+"--------------------------------------")
        print(e)
        return my_rtc
    print(response)
    print(response["datetime"])
    current_time = response["datetime"]
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]

    # We can also fill in these extra nice things
    year_day = response["day_of_year"]
    week_day = response["day_of_week"]
    is_dst = response["dst"]

    now = time.struct_time(
        (year, month, mday, hours, minutes, seconds, week_day, year_day, is_dst)
    )
    print(now)
    my_rtc.datetime = now
    return my_rtc


def get_flight_details(fn, requests):
    byte_counter=0
    chunk_length=1024
    success=False

    # zero out any old data in the byte array
    for i in range(0,json_size):
        json_bytes[i]=0

    # Get the URL response one chunk at a time
    try:
        response=requests.get(url=FLIGHT_LONG_DETAILS_HEAD+str(fn),headers=constants.rheaders)
        for chunk in response.iter_content(chunk_size=chunk_length):
            # if the chunk will fit in the byte array, add it
            if(byte_counter+chunk_length<=json_size):
                for i in range(0,len(chunk)):
                    json_bytes[i+byte_counter]=chunk[i]
            else:
                print("Exceeded max string size while parsing JSON")
                return False

            byte_counter+=len(chunk)
            # find the comma before trail
            trail_start=json_bytes.find((b",\"trail\":"))
            if trail_start != -1:
                json_bytes[trail_start] = ord(b"}")
                for i in range(trail_start + 1, byte_counter):
                    json_bytes[i] = 0
                print("Details lookup saved "+str(trail_start)+" bytes.")
                return True

         
    except Exception as e:
            print("Error--------------------------------------------------")
            print(e)
            return False

    #If we got here we got through all the JSON without finding the right trail entries
    print("Failed to find a valid trail entry in JSON")
    return False



def parse_details_json():
    try:
        # get the JSON from the bytes
        long_json=json.loads(json_bytes)

        # Some available values from the JSON. Put the details URL and a flight ID in your browser and have a look for more.

        flight_number=long_json["identification"]["number"]["default"]
        #print(flight_number)
        flight_callsign=long_json["identification"]["callsign"]
        aircraft_code=long_json["aircraft"]["model"]["code"]
        aircraft_model=long_json["aircraft"]["model"]["text"]
        #aircraft_registration=long_json["aircraft"]["registration"]
        airline_name=long_json["airline"]["name"]
        print("airline name: ", airline_name)
        constants.airline_name = airline_name
        #airline_short=long_json["airline"]["short"]
        airport_origin_name=long_json["airport"]["origin"]["name"]
        airport_origin_name = airport_origin_name.replace(" International", "")
        airport_origin_name=airport_origin_name.replace(" Airport","")
        airport_origin_code=long_json["airport"]["origin"]["code"]["iata"]
        #airport_origin_country=long_json["airport"]["origin"]["position"]["country"]["name"]
        #airport_origin_country_code=long_json["airport"]["origin"]["position"]["country"]["code"]
        #airport_origin_city=long_json["airport"]["origin"]["position"]["region"]["city"]
        #airport_origin_terminal=long_json["airport"]["origin"]["info"]["terminal"]
        airport_destination_name=long_json["airport"]["destination"]["name"]
        airport_destination_name=airport_destination_name.replace(" Airport","")
        airport_destination_name = airport_destination_name.replace(" International", "")
        airport_destination_code=long_json["airport"]["destination"]["code"]["iata"]
        #airport_destination_country=long_json["airport"]["destination"]["position"]["country"]["name"]
        #airport_destination_country_code=long_json["airport"]["destination"]["position"]["country"]["code"]
        #airport_destination_city=long_json["airport"]["destination"]["position"]["region"]["city"]
        #airport_destination_terminal=long_json["airport"]["destination"]["info"]["terminal"]
        #time_scheduled_departure=long_json["time"]["scheduled"]["departure"]
        #time_real_departure=long_json["time"]["real"]["departure"]
        #time_scheduled_arrival=long_json["time"]["scheduled"]["arrival"]
        #time_estimated_arrival=long_json["time"]["estimated"]["arrival"]
        #latitude=long_json["trail"][0]["lat"]
        #longitude=long_json["trail"][0]["lng"]
        #altitude=long_json["trail"][0]["alt"]
        #speed=long_json["trail"][0]["spd"]
        #heading=long_json["trail"][0]["hd"]

        
        if flight_number:
            print("Flight is called "+flight_number)
        elif flight_callsign:
            print("No flight number, callsign is "+flight_callsign)
        else:
            print("No number or callsign for this flight.")


        # Set up to 6 of the values above as text for display_flights to put on the screen
        # Short strings get placed on screen, then longer ones scroll over each in sequence

        constants.label1_short=flight_number if flight_number else flight_callsign
        constants.label1_long=airline_name
        constants.label2_short=airport_origin_code+"-"+airport_destination_code
        constants.label2_long=airport_origin_name+"-"+airport_destination_name
        constants.label3_short=aircraft_code
        constants.label3_long=aircraft_model

        if not constants.label1_short:
            constants.label1_short=''
        if not constants.label1_long:
            constants.label1_long=''
        if not constants.label2_short:
            constants.label2_short=''
        if not constants.label2_long:
            constants.label2_long=''
        if not constants.label3_short:
            constants.label3_short=''
        if not constants.label3_long:
            constants.label3_long=''

    except (KeyError, ValueError,TypeError) as e:
            print("JSON error")
            print (e)
            return False

    return True