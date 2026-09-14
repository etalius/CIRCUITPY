import time
import gc
from microcontroller import watchdog as w
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
import displayio
import constants
import internet

_at = 0
vis_km = constants.DEFAULT_VIS_KM
_temp = None
_high = None
_low = None
_code = 0
_ok = False

ICON = 12
SUN = (
    (0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0),
    (0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0),
    (0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0),
)
CLOUD = (
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
)
RAIN = (
    (0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0),
    (0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
)
SNOW = (
    (0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0),
    (0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1),
    (0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
)
PARTLY = (
    (0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 0, 0, 2, 2, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0),
    (0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2),
    (1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2),
    (0, 0, 1, 1, 0, 2, 2, 2, 2, 2, 2, 2),
    (0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2, 0),
    (0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
)


def _icon_for(code):
    if code <= 0:
        return SUN, (0xFCD34D,)
    if code <= 2:
        return PARTLY, (0xFCD34D, 0x9CA3AF)
    if code <= 3 or code in (45, 48):
        return CLOUD, (0x9CA3AF,)
    if 71 <= code <= 77 or 85 <= code <= 86:
        return SNOW, (0xE5E7EB,)
    return RAIN, (0x60A5FA,)


def _num(value):
    return int(round(float(value)))


def _first(value):
    if isinstance(value, list):
        return value[0]
    return value


def ensure(requests):
    global _at, vis_km, _temp, _high, _low, _code, _ok
    now = time.monotonic()
    if _ok and _at and (now - _at) < constants.VIS_CACHE_S:
        return True
    response_raw = None
    try:
        w.feed()
        response_raw = requests.get(url=constants.WEATHER_URL)
        data = response_raw.json()
        print("weather json", data)
        current = data["current"] if "current" in data else data["current_weather"]
        daily = data["daily"]
        if "temperature_2m" in current:
            _temp = _num(current["temperature_2m"])
        else:
            _temp = _num(current["temperature"])
        if "weather_code" in current:
            _code = _num(current["weather_code"])
        else:
            _code = _num(current["weathercode"])
        _high = _num(_first(daily["temperature_2m_max"]))
        _low = _num(_first(daily["temperature_2m_min"]))
        if "visibility" in current and current["visibility"] is not None:
            vis_km = max(1.0, float(current["visibility"]) / 1000.0)
        _ok = True
        _at = now
        print("weather parsed", _temp, _high, _low, _code, "vis", vis_km)
        return True
    except Exception as e:
        print("weather lookup failed", e.__class__.__name__, e)
        if not _ok:
            vis_km = constants.DEFAULT_VIS_KM
        return _ok
    finally:
        internet.close_response(response_raw)
        w.feed()


def show(display, hours, minutes):
    group = displayio.Group()
    gc.collect()

    if _ok:
        icon, colors = _icon_for(_code)
        bmp = displayio.Bitmap(ICON, ICON, 1 + len(colors))
        pal = displayio.Palette(1 + len(colors))
        pal[0] = 0x000000
        for i, color in enumerate(colors):
            pal[i + 1] = color
        for row in range(ICON):
            for col in range(ICON):
                bmp[col, row] = icon[row][col]
        tg = displayio.TileGrid(bmp, pixel_shader=pal)
        group.append(tg)

        clock_font = bitmap_font.load_font("IBMPlexMono-Medium-24_jep.bdf")
        temp = Label(clock_font, color=0xFFFFFF, text=str(_temp))
        deg = Label(constants.font, color=0xFFFFFF, text="\u00b0")
        hi = Label(constants.font, color=0xEE82EE, text="H" + str(_high))
        lo = Label(constants.font, color=0x57B9FF, text="L" + str(_low))
        _, _, tw, _ = temp.bounding_box
        _, _, hw, _ = hi.bounding_box
        _, _, lw, _ = lo.bounding_box
        rail = hw if hw > lw else lw
        gap = 3
        icon_w = ICON
        total = icon_w + gap + tw + gap + rail
        x0 = (display.width - total) // 2
        if x0 < 1:
            x0 = 1
        tg.x = x0
        tg.y = (display.height - ICON) // 2
        temp.x = x0 + icon_w + gap
        temp.y = display.height // 2
        deg.x = temp.x + tw - 1
        deg.y = display.height // 2 - 8
        rail_x = temp.x + tw + gap
        if rail_x + rail > display.width - 1:
            rail_x = display.width - 1 - rail
        hi.x = rail_x
        lo.x = rail_x
        hi.y = display.height // 2 - 6
        lo.y = display.height // 2 + 6
        group.append(temp)
        group.append(deg)
        group.append(hi)
        group.append(lo)
        gc.collect()
    else:
        msg = Label(constants.font, color=0xFFFFFF, text="no wx")
        _, _, bw, _ = msg.bounding_box
        msg.x = round(display.width / 2 - bw / 2)
        msg.y = display.height // 2
        group.append(msg)

    display.root_group = group
