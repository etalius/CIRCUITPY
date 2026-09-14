import math
import time
from microcontroller import watchdog as w
import constants
import internet
import weather

_vis_km = 10.0
_vis_at = 0


def _wrap180(deg):
    while deg > 180:
        deg -= 360
    while deg < -180:
        deg += 360
    return deg


def _dest(lat, lon, bearing_deg, dist_km):
    d = dist_km / 6371.0
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    brg = math.radians(bearing_deg)
    lat2 = math.asin(
        math.sin(lat1) * math.cos(d)
        + math.cos(lat1) * math.sin(d) * math.cos(brg)
    )
    lon2 = lon1 + math.atan2(
        math.sin(brg) * math.sin(d) * math.cos(lat1),
        math.cos(d) - math.sin(lat1) * math.sin(lat2),
    )
    return math.degrees(lat2), math.degrees(lon2)


def _bearing(lat1, lon1, lat2, lon2):
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dlon = math.radians(lon2 - lon1)
    y = math.sin(dlon) * math.cos(p2)
    x = (
        math.cos(p1) * math.sin(p2)
        - math.sin(p1) * math.cos(p2) * math.cos(dlon)
    )
    return (math.degrees(math.atan2(y, x)) + 360) % 360


def _dist_km(lat1, lon1, lat2, lon2):
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dlat = p2 - p1
    dlon = math.radians(lon2 - lon1)
    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    )
    return 2 * 6371.0 * math.asin(math.sqrt(min(1.0, h)))


def _elev_deg(alt_ft, dist_km):
    alt_m = max(0.0, alt_ft) * 0.3048
    return math.degrees(math.atan2(alt_m, max(80.0, dist_km * 1000.0)))


def _slant_km(alt_ft, dist_km):
    alt_km = max(0.0, alt_ft) * 0.0003048
    return math.sqrt(dist_km * dist_km + alt_km * alt_km)


def range_km():
    # Farthest ground range where a plane in our alt band can still sit in
    # the window: above the sill, below the header, and inside visibility.
    vis = max(1.0, _vis_km)
    tan_lo = math.tan(math.radians(constants.MIN_ELEV_DEG))
    tan_hi = math.tan(math.radians(constants.MAX_ELEV_DEG))
    best = constants.MIN_RANGE_KM
    for alt_ft in (1500.0, 3500.0, 8000.0, 18000.0, 35000.0):
        if alt_ft < constants.MIN_ALT_FT or alt_ft > constants.MAX_ALT_FT:
            continue
        alt_km = alt_ft * 0.0003048
        if alt_km >= vis:
            continue
        d_vis = math.sqrt(vis * vis - alt_km * alt_km)
        d_far = alt_km / tan_lo if tan_lo > 0 else vis
        d = min(d_vis, d_far, constants.MAX_RANGE_KM)
        d_near = alt_km / tan_hi if tan_hi > 0 else 0.0
        if d > d_near and d > best:
            best = d
    return min(constants.MAX_RANGE_KM, max(constants.MIN_RANGE_KM, best))


def update_visibility(requests):
    global _vis_km, _vis_at
    weather.ensure(requests)
    if weather.vis_km:
        _vis_km = weather.vis_km
        _vis_at = time.monotonic()
    elif not _vis_at:
        _vis_km = constants.DEFAULT_VIS_KM
        _vis_at = time.monotonic()
    return _vis_km


def bounds_box():
    r = range_km()
    half = constants.VIEW_FOV_DEG / 2.0
    face = constants.FACE_DEG
    lats = [constants.HOME_LAT]
    lons = [constants.HOME_LON]
    near = _dest(constants.HOME_LAT, constants.HOME_LON, face + 180, 0.4)
    lats.append(near[0])
    lons.append(near[1])
    for offset in (-half, -half / 2, 0, half / 2, half):
        p = _dest(constants.HOME_LAT, constants.HOME_LON, face + offset, r)
        lats.append(p[0])
        lons.append(p[1])
    north = max(lats)
    south = min(lats)
    west = min(lons)
    east = max(lons)
    return "{:.3f},{:.3f},{:.3f},{:.3f}".format(north, south, west, east)


def feed_url():
    return (
        constants.FLIGHT_SEARCH_HEAD
        + bounds_box()
        + constants.FLIGHT_SEARCH_TAIL
    )


def _span_m(code, alt_ft):
    t = (code or "").strip().upper()
    if t.startswith((
        "C15", "C16", "C17", "C18", "C20", "C21",
        "PA2", "PA3", "PA4", "SR2", "M20", "RV",
        "CH7", "DA2", "DA4", "P28", "C72",
    )):
        return 11.0
    if t.startswith(("C25", "C56", "C68", "E55", "CL3", "BE4", "H25", "LJ", "C51")):
        return 18.0
    if t.startswith(("B77", "B78", "A33", "A35", "A38", "B74")):
        return 60.0
    if t.startswith(("B73", "B75", "B76", "A31", "A32", "A21", "E17", "E19", "E75", "BCS")):
        return 34.0
    if alt_ft < 4000:
        return 12.0
    if alt_ft < 12000:
        return 20.0
    return 35.0


def _apparent_deg(span_m, slant_km):
    return math.degrees(math.atan2(span_m, max(80.0, slant_km * 1000.0)))


def _in_window(dist, off, alt_ft, elev, code):
    if alt_ft < constants.MIN_ALT_FT:
        return False
    slant = _slant_km(alt_ft, dist)
    if slant > _vis_km * 1.05:
        return False
    if _apparent_deg(_span_m(code, alt_ft), slant) < constants.MIN_APPARENT_DEG:
        return False
    if off > (constants.VIEW_FOV_DEG / 2.0):
        return False
    if dist <= constants.OVERHEAD_KM:
        return True
    return constants.MIN_ELEV_DEG <= elev <= constants.MAX_ELEV_DEG


def _score(dist, off, elev):
    # Lower is better: close, ahead, and well up in the window.
    align = max(0.2, math.cos(math.radians(off)))
    lift = max(0.2, math.sin(math.radians(max(elev, 0.0))))
    return dist / (align * lift)


def pick_flight(response):
    best = None
    best_score = None
    for flight_id, info in response.items():
        if flight_id in constants.SKIP_FEED_KEYS:
            continue
        if not isinstance(info, list) or len(info) < 5:
            continue
        try:
            lat = float(info[1])
            lon = float(info[2])
        except (TypeError, ValueError):
            continue
        on_ground = info[14] if len(info) > 14 else 0
        if on_ground:
            continue
        dist = _dist_km(constants.HOME_LAT, constants.HOME_LON, lat, lon)
        brg = _bearing(constants.HOME_LAT, constants.HOME_LON, lat, lon)
        signed = _wrap180(brg - constants.FACE_DEG)
        off = abs(signed)
        try:
            alt_ft = float(info[4])
        except (TypeError, ValueError, IndexError):
            alt_ft = 0
        elev = _elev_deg(alt_ft, dist)
        ac = info[8] if len(info) > 8 else ""
        if not _in_window(dist, off, alt_ft, elev, ac):
            continue
        score = _score(dist, off, elev)
        picked = (flight_id, info, dist, signed, brg, alt_ft, elev)
        if best_score is None or score < best_score:
            best = picked
            best_score = score
    if not best:
        return None
    flight_id, info, dist, signed, brg, alt_ft, elev = best
    try:
        hdg = float(info[3])
    except (TypeError, ValueError, IndexError):
        hdg = constants.FACE_DEG
    constants.plane_off_deg = signed
    constants.plane_elev_deg = elev
    constants.plane_dist_km = dist
    constants.plane_hdg_deg = hdg
    print(
        "picked",
        flight_id,
        "km",
        round(dist, 1),
        "off",
        int(signed),
        "elev",
        int(elev),
        "hdg",
        int(hdg),
        "brg",
        int(brg),
    )
    return flight_id, info
