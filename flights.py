
from microcontroller import watchdog as w
import constants
import json
import time
import internet
import lookups

json_size = 7_000
json_bytes = bytearray(json_size)

SKIP_FEED_KEYS = ("version", "full_count", "stats")

FLIGHT_LONG_DETAILS_HEAD="https://data-live.flightradar24.com/clickhandler/?flight="


def _text(value):
    if value is None:
        return ""
    return str(value).strip()


def apply_feed_labels(info):
    aircraft_code = _text(info[8]) if len(info) > 8 else ""
    origin = _text(info[11]) if len(info) > 11 else ""
    dest = _text(info[12]) if len(info) > 12 else ""
    flight_number = _text(info[13]) if len(info) > 13 else ""
    callsign = _text(info[16]) if len(info) > 16 else ""
    airline_icao = _text(info[18]) if len(info) > 18 else ""
    airline = lookups.airline_name(airline_icao)

    constants.airline_name = airline
    constants.label1_short = flight_number if flight_number else callsign
    constants.label1_long = airline

    if dest and dest == origin:
        dest = ""
    if origin and dest:
        constants.label2_short = origin + "-" + dest
        constants.label2_long = lookups.airport_name(origin) + "-" + lookups.airport_name(dest)
    else:
        one = origin or dest
        name = lookups.airport_name(one) if one else ""
        # 64px panel ~11 glyphs; keep a single airport centered.
        constants.label2_short = name if name and len(name) <= 11 else one
        constants.label2_long = constants.label2_short

    constants.label3_short = aircraft_code
    constants.label3_long = lookups.aircraft_name(aircraft_code) if aircraft_code else ""


def _pick_flight(response):
    fallback = None
    for flight_id, flight_info in response.items():
        if flight_id in SKIP_FEED_KEYS:
            continue
        if not isinstance(flight_info, list) or len(flight_info) < 8:
            continue
        on_ground = flight_info[14] if len(flight_info) > 14 else 0
        flight_number = _text(flight_info[13]) if len(flight_info) > 13 else ""
        if on_ground:
            continue
        picked = (flight_id, flight_info)
        if flight_number:
            return picked
        if fallback is None:
            fallback = picked
    return fallback


def get_flights(matrixportal, requests):
    matrixportal.url = constants.FLIGHT_SEARCH_URL
    response_raw = None
    try:
        response_raw = requests.get(url=constants.FLIGHT_SEARCH_URL, headers=constants.rheaders)
        response = response_raw.json()
    except Exception as e:
        print(e.__class__.__name__ + "--------------------------------------")
        print(e)
        return False
    finally:
        internet.close_response(response_raw)

    print(response)
    if not isinstance(response, dict):
        print("Unexpected flight feed payload")
        return False

    picked = _pick_flight(response)
    if not picked:
        return None

    flight_id, flight_info = picked
    print(flight_id)
    apply_feed_labels(flight_info)

    timestamp = flight_info[10] if len(flight_info) > 10 else 0
    try:
        if constants.IS_DST:
            adjusted_time = time.localtime(timestamp - (7 * 3600))
        else:
            adjusted_time = time.localtime(timestamp - (8 * 3600))
    except Exception:
        adjusted_time = None
    return flight_id, adjusted_time


def new_get_time(matrixportal, requests, my_rtc):
    new_url = 'http://api.timezonedb.com/v2.1/get-time-zone?key=EPWKTIIIXP9B&format=json&by=zone&zone=America/Los_Angeles'
    matrixportal.url = new_url
    response_raw = None
    try:
        response_raw = requests.get(url=new_url)
        response = response_raw.json()
    except Exception as e:
        print(e.__class__.__name__+"--------------------------------------")
        print(e)
        return my_rtc
    finally:
        internet.close_response(response_raw)

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
    response_raw = None
    try:
        response_raw = requests.get(url="http://worldtimeapi.org/api/ip")
        response = response_raw.json()
    except Exception as e:
        print(e.__class__.__name__+"--------------------------------------")
        print(e)
        return my_rtc
    finally:
        internet.close_response(response_raw)
    print(response)
    print(response["datetime"])
    current_time = response["datetime"]
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]

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
    response=None

    for i in range(0,json_size):
        json_bytes[i]=0

    try:
        response=requests.get(url=FLIGHT_LONG_DETAILS_HEAD+str(fn),headers=constants.rheaders)
        status = getattr(response, "status_code", 200)
        if status and int(status) >= 400:
            print("Details lookup HTTP", status)
            return False
        for chunk in response.iter_content(chunk_size=chunk_length):
            w.feed()
            if(byte_counter+chunk_length<=json_size):
                for i in range(0,len(chunk)):
                    json_bytes[i+byte_counter]=chunk[i]
            else:
                print("Exceeded max string size while parsing JSON")
                return False

            byte_counter+=len(chunk)
            trail_start=json_bytes.find((b",\"flightHistory\":"))
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
    finally:
        internet.close_response(response)

    print("Failed to find a valid trail entry in JSON")
    return False


def parse_details_json():
    try:
        long_json=json.loads(json_bytes)

        flight_number=long_json["identification"]["number"]["default"]
        flight_callsign=long_json["identification"]["callsign"]
        aircraft_code=long_json["aircraft"]["model"]["code"]
        aircraft_model=long_json["aircraft"]["model"]["text"]
        airline_name=long_json["airline"]["name"]
        print("airline name: ", airline_name)
        constants.airline_name = airline_name
        airport_origin_name=long_json["airport"]["origin"]["name"]
        airport_origin_name = airport_origin_name.replace(" International", "")
        airport_origin_name=airport_origin_name.replace(" Airport","")
        airport_origin_code=long_json["airport"]["origin"]["code"]["iata"]
        airport_destination_name=long_json["airport"]["destination"]["name"]
        airport_destination_name=airport_destination_name.replace(" Airport","")
        airport_destination_name = airport_destination_name.replace(" International", "")
        airport_destination_code=long_json["airport"]["destination"]["code"]["iata"]

        if flight_number:
            print("Flight is called "+flight_number)
        elif flight_callsign:
            print("No flight number, callsign is "+flight_callsign)
        else:
            print("No number or callsign for this flight.")

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
