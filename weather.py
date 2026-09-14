import time
import math
import gc
from microcontroller import watchdog as w
from adafruit_display_text.label import Label
import displayio
import constants
import internet

_at = 0
vis_km = constants.DEFAULT_VIS_KM
_temp = 0
_high = 0
_low = 0
_code = 0
_ok = False

ICON = 16
SUN = (
    (0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0),
    (0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0),
)
MOON = (
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
)
CLOUD = (
    (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
)
RAIN = (
    (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0),
    (1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
)
SNOW = (
    (0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0),
    (1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0),
    (0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0),
)
PARTLY = (
    (0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 0, 2, 2, 0, 0, 0),
    (0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0),
    (0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0),
    (1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 2, 2),
    (0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2),
    (0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0),
    (0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0),
)
HORIZON = (
    (0, 1, 0, 0, 1, 0, 0, 1, 0),
    (0, 0, 0, 1, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 0, 0),
    (0, 0, 0, 1, 1, 1, 0, 0, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1),
)
DIGIT_W = 7
DIGIT_H = 12
DIGIT_DW = 8
DIGIT_DH = 14
DIGITS = {
    "0": (
        ".#####.",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        ".#####.",
    ),
    "1": (
        "...##..",
        "..###..",
        "...##..",
        "...##..",
        "...##..",
        "...##..",
        "...##..",
        "...##..",
        "...##..",
        "...##..",
        "...##..",
        ".######",
    ),
    "2": (
        ".#####.",
        "##...##",
        ".....##",
        ".....##",
        "....##.",
        "...##..",
        "..##...",
        ".##....",
        "##.....",
        "##.....",
        "##.....",
        "#######",
    ),
    "3": (
        ".#####.",
        "##...##",
        ".....##",
        ".....##",
        "..####.",
        ".....##",
        ".....##",
        ".....##",
        ".....##",
        ".....##",
        "##...##",
        ".#####.",
    ),
    "4": (
        "....##.",
        "...###.",
        "..#.##.",
        ".#..##.",
        "##..##.",
        "##..##.",
        "#######",
        "....##.",
        "....##.",
        "....##.",
        "....##.",
        "....##.",
    ),
    "5": (
        "#######",
        "##.....",
        "##.....",
        "##.....",
        "######.",
        ".....##",
        ".....##",
        ".....##",
        ".....##",
        ".....##",
        "##...##",
        ".#####.",
    ),
    "6": (
        ".#####.",
        "##...##",
        "##.....",
        "##.....",
        "######.",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        ".#####.",
    ),
    "7": (
        "#######",
        ".....##",
        ".....##",
        "....#..",
        "...#...",
        "...#...",
        "..##...",
        "..##...",
        "..##...",
        "..##...",
        "..##...",
        "..##...",
    ),
    "8": (
        ".#####.",
        "##...##",
        "##...##",
        "##...##",
        ".#####.",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        ".#####.",
    ),
    "9": (
        ".#####.",
        "##...##",
        "##...##",
        "##...##",
        "##...##",
        ".######",
        ".....##",
        ".....##",
        ".....##",
        ".....##",
        "##...##",
        ".#####.",
    ),
    "-": (
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
        "#######",
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
        ".......",
    ),
}
DEG = (
    (0, 1, 0),
    (1, 0, 1),
    (0, 1, 0),
)
TINY = {
    "0": ("111", "101", "101", "101", "111"),
    "1": ("010", "110", "010", "010", "111"),
    "2": ("111", "001", "111", "100", "111"),
    "3": ("111", "001", "111", "001", "111"),
    "4": ("101", "101", "111", "001", "001"),
    "5": ("111", "100", "111", "001", "111"),
    "6": ("111", "100", "111", "101", "111"),
    "7": ("111", "001", "010", "010", "010"),
    "8": ("111", "101", "111", "101", "111"),
    "9": ("111", "101", "111", "001", "111"),
    ":": ("0", "1", "0", "1", "0"),
}


def _scale(src, nw, nh):
    oh = len(src)
    ow = len(src[0])
    out = []
    for y in range(nh):
        sy = y * oh // nh
        row = []
        for x in range(nw):
            sx = x * ow // nw
            row.append(src[sy][sx])
        out.append(tuple(row))
    return tuple(out)


def _icon_for(code, night):
    if code <= 0:
        if night:
            return MOON, (0xE5E7EB,)
        return _scale(SUN, ICON, ICON), (0xFCD34D,)
    if code <= 2:
        return _scale(PARTLY, ICON, ICON), (0xFCD34D, 0x9CA3AF)
    if code <= 3 or code in (45, 48):
        return _scale(CLOUD, ICON, ICON), (0x9CA3AF,)
    if 71 <= code <= 77 or 85 <= code <= 86:
        return _scale(SNOW, ICON, ICON), (0xE5E7EB,)
    return _scale(RAIN, ICON, ICON), (0x60A5FA,)


def _num(value):
    return int(round(float(value)))


def _first(value):
    if isinstance(value, list):
        return value[0]
    return value


def _sun_mins(yday):
    wave = math.cos((yday - 172) * 0.017214)
    rise = int((6.55 + 0.73 * wave) * 60)
    sett = int((18.75 - 1.80 * wave) * 60)
    return rise, sett


def _fmt_hm(mins):
    h24 = (mins // 60) % 24
    m = mins % 60
    h = h24
    if h24 == 0:
        h = 12
    elif h24 > 12:
        h = h24 - 12
    return str(h) + ":" + ("0" + str(m))[-2:]


def _next_sun(hours, minutes, yday):
    now = hours * 60 + minutes
    rise, sett = _sun_mins(yday)
    night = now < rise or now >= sett
    if now < rise or now >= sett:
        return night, _fmt_hm(rise)
    return night, _fmt_hm(sett)


def _tiny_rows(text):
    glyphs = []
    for ch in text:
        g = TINY.get(ch)
        if g:
            glyphs.append(g)
    if not glyphs:
        return (("0",),)
    rows = []
    for r in range(5):
        parts = [g[r] for g in glyphs]
        rows.append("0".join(parts))
    return tuple(rows)


def _tiny_pixels(text):
    return tuple(tuple(1 if c == "1" else 0 for c in row) for row in _tiny_rows(text))


def ensure(requests):
    global _at, vis_km, _temp, _high, _low, _code, _ok
    now = time.monotonic()
    if _ok and _at and (now - _at) < constants.VIS_CACHE_S:
        return True
    response_raw = None
    try:
        w.feed()
        response_raw = requests.get(url=constants.WEATHER_URL)
        w.feed()
        data = response_raw.json()
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
        print("wx", _temp, _high, _low, _code)
        return True
    except Exception as e:
        print("wx fail", e.__class__.__name__)
        if not _ok:
            vis_km = constants.DEFAULT_VIS_KM
        return _ok
    finally:
        internet.close_response(response_raw)
        w.feed()


def _tile(pixels, colors, x, y, group):
    h = len(pixels)
    wd = len(pixels[0])
    bmp = displayio.Bitmap(wd, h, 1 + len(colors))
    pal = displayio.Palette(1 + len(colors))
    pal[0] = 0x000000
    for i, color in enumerate(colors):
        pal[i + 1] = color
    for row in range(h):
        prow = pixels[row]
        for col in range(wd):
            bmp[col, row] = prow[col] if col < len(prow) else 0
    tg = displayio.TileGrid(bmp, pixel_shader=pal, x=x, y=y)
    group.append(tg)
    return tg


def _digit_glyph(ch):
    raw = DIGITS.get(ch, DIGITS["0"])
    src = tuple(tuple(1 if pix == "#" else 0 for pix in row) for row in raw)
    return _scale(src, DIGIT_DW, DIGIT_DH)


def _temp_sprite(text):
    chars = str(text)
    gap = 1
    deg_gap = 2
    deg_w = 3
    n = len(chars)
    width = n * DIGIT_DW + max(0, n - 1) * gap + deg_gap + deg_w
    glyphs = [_digit_glyph(ch) for ch in chars]
    rows = []
    for y in range(DIGIT_DH):
        line = []
        for i, glyph in enumerate(glyphs):
            line.extend(glyph[y])
            if i + 1 < n:
                line.append(0)
        for _ in range(deg_gap):
            line.append(0)
        if y < 3:
            line.extend(DEG[y])
        while len(line) < width:
            line.append(0)
        rows.append(tuple(line[:width]))
    return tuple(rows)


def show(display, hours, minutes):
    try:
        _show(display, hours, minutes)
    except Exception as e:
        print("wx show", e.__class__.__name__)


def _show(display, hours, minutes):
    group = displayio.Group()
    gc.collect()
    w.feed()
    if not _ok:
        msg = Label(constants.font, color=0xFFFFFF, text="no wx")
        _, _, bw, _ = msg.bounding_box
        msg.x = (display.width - bw) // 2
        msg.y = display.height // 2
        group.append(msg)
        display.root_group = group
        return

    yday = time.localtime().tm_yday
    night, sun_txt = _next_sun(hours, minutes, yday)
    icon, colors = _icon_for(_code, night)
    col_w = ICON
    col_x = 1
    _tile(icon, colors, col_x, 1, group)

    time_px = _tiny_pixels(sun_txt)
    time_w = len(time_px[0])
    hz_w = len(HORIZON[0])
    if time_w > col_w:
        col_w = time_w
    _tile(HORIZON, (0xFCD34D,), col_x + (col_w - hz_w) // 2, 19, group)
    _tile(time_px, (0xFCD34D,), col_x + (col_w - time_w) // 2, 25, group)

    hi = Label(constants.font, color=0xEE82EE, text="H" + str(_high))
    lo = Label(constants.font, color=0x57B9FF, text="L" + str(_low))
    _, _, hw, _ = hi.bounding_box
    _, _, lw, _ = lo.bounding_box
    rail = hw if hw > lw else lw
    rail_x = display.width - 1 - rail
    hi.x = rail_x
    lo.x = rail_x
    hi.y = 7
    lo.y = 25
    group.append(hi)
    group.append(lo)

    temp_px = _temp_sprite(_temp)
    tw = len(temp_px[0])
    left = col_x + col_w + 2
    avail = rail_x - 2 - left
    x0 = left + (avail - tw) // 2
    if x0 + tw > rail_x - 1:
        x0 = rail_x - 1 - tw
    if x0 < col_x + 1:
        x0 = col_x + 1
    _tile(temp_px, (0xFFFFFF,), x0, (display.height - DIGIT_DH) // 2, group)

    display.root_group = group
    gc.collect()
    w.feed()
