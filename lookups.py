# Packed name table on disk so we do not keep a dict in RAM.
# lookups.dat: 10-byte header, then sorted 20-byte records (4-char key + name).

REC = 20
_HDR = None


def _header():
    global _HDR
    if _HDR is not None:
        return _HDR
    with open("lookups.dat", "rb") as f:
        if f.read(4) != b"LK01":
            _HDR = (0, 0, 0)
            return _HDR
        n_air = int.from_bytes(f.read(2), "little")
        n_ac = int.from_bytes(f.read(2), "little")
        n_al = int.from_bytes(f.read(2), "little")
    _HDR = (n_air, n_ac, n_al)
    return _HDR


def _lookup(code, start, count):
    if not code or count <= 0:
        return ""
    key = (code.strip().upper() + "    ")[:4]
    key_b = key.encode()
    with open("lookups.dat", "rb") as f:
        lo = 0
        hi = count
        while lo < hi:
            mid = (lo + hi) // 2
            f.seek(10 + (start + mid) * REC)
            rec = f.read(REC)
            rec_key = rec[:4]
            if rec_key == key_b:
                return rec[4:].split(b"\x00", 1)[0].decode()
            if rec_key < key_b:
                lo = mid + 1
            else:
                hi = mid
    return code.strip().upper()


def airport_name(code):
    n_air, n_ac, n_al = _header()
    return _lookup(code, 0, n_air) or code


def aircraft_name(code):
    n_air, n_ac, n_al = _header()
    return _lookup(code, n_air, n_ac) or code


def airline_name(code):
    n_air, n_ac, n_al = _header()
    return _lookup(code, n_air + n_ac, n_al) or code
