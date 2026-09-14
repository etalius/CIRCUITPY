import terminalio

# Display constants
font = terminalio.FONT

# Window: 37°24'17.6"N 122°06'48.7"W, 5th floor, facing Del Medio Ave.
HOME_LAT = 37.404889
HOME_LON = -122.113528
FACE_DEG = 310.0
VIEW_FOV_DEG = 110.0
EYE_HEIGHT_M = 17.0
MIN_RANGE_KM = 3.5
MAX_RANGE_KM = 18.0
DEFAULT_VIS_KM = 10.0
OVERHEAD_KM = 1.4
MIN_ELEV_DEG = 2.5
MAX_ELEV_DEG = 42.0
MIN_ALT_FT = 1500.0
MAX_ALT_FT = 42000.0
MIN_APPARENT_DEG = 0.16
VIS_CACHE_S = 900
SKIP_FEED_KEYS = ("version", "full_count", "stats")
VIS_URL = "http://api.open-meteo.com/v1/forecast?latitude=37.41&longitude=-122.11&current_weather=true"
WEATHER_URL = "http://api.open-meteo.com/v1/forecast?latitude=37.41&longitude=-122.11&temperature_unit=fahrenheit&current=temperature_2m,weather_code,visibility&daily=temperature_2m_max,temperature_2m_min&forecast_days=1"
QUERY_DELAY=5
FLIGHT_SEARCH_HEAD="https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds="
FLIGHT_SEARCH_TAIL="&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=0&air=1&vehicles=0&estimated=0&maxage=14400&gliders=0&stats=0&ems=1&limit=15"
rheaders = {
     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0",
     "cache-control": "no-store, no-cache, must-revalidate",
     "accept": "application/json",
     "Origin": "https://www.flightradar24.com",
     "Referer": "https://www.flightradar24.com/",
}

# Plane Animation constants
PLANE_SPEED=0.04
PLANE_COLOUR=0x4B0082

# Test constants
ROW_ONE_COLOUR=0xEE82EE
ROW_TWO_COLOUR=	0xD3D3D3 #0x4B0082
ROW_THREE_COLOUR=0x57B9FF #0xFFA500
TEXT_SPEED=0.04
PAUSE_BETWEEN_LABEL_SCROLLING=3

IS_DST = False

# Globals
def init_globals():
    global label1_short
    label1_short = ""

    global label2_short
    label2_short = ""

    global label3_short
    label3_short = ""

    global label1_long
    label1_long = ""

    global label2_long
    label2_long = ""

    global label3_long
    label3_long = ""

    global airline_name
    airline_name = ""

    global plane_off_deg
    plane_off_deg = 0.0

    global plane_elev_deg
    plane_elev_deg = 0.0

    global plane_dist_km
    plane_dist_km = 0.0

    global plane_hdg_deg
    plane_hdg_deg = 0.0
