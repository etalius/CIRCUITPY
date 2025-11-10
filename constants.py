import terminalio

# Display constants
font = terminalio.FONT

# Constants for pinging flightrader
BOUNDS_BOX= '37.489,37.401,-122.212,-122.105' # SFO '37.64,37.59,-122.40,-122.35' 
QUERY_DELAY=5
FLIGHT_SEARCH_HEAD="https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds="
FLIGHT_SEARCH_TAIL="&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=0&air=1&vehicles=0&estimated=0&maxage=14400&gliders=0&stats=0&ems=1&limit=1"
FLIGHT_SEARCH_URL=FLIGHT_SEARCH_HEAD+BOUNDS_BOX+FLIGHT_SEARCH_TAIL
rheaders = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
     "cache-control": "no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
     "accept": "application/json"
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



