import displayio

ARRAY_SIZE = 20
BITS_PER_ELEMENT = 2

# UNITED = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# , [0, 1, 1, 2, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# , [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# , [2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0]
# , [2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0]
# , [1, 2, 2, 2, 1, 3, 3, 3, 1, 2, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0]
# , [2, 2, 2, 1, 1, 1, 0, 1, 1, 3, 3, 3, 1, 0, 2, 0, 0, 0, 0, 0]
# , [2, 1, 2, 2, 2, 3, 2, 0, 1, 1, 1, 2, 3, 2, 2, 2, 0, 0, 0, 0]
# , [3, 2, 0, 0, 2, 2, 3, 3, 2, 2, 0, 0, 2, 3, 2, 2, 0, 0, 0, 0]
# , [0, 3, 2, 2, 1, 0, 0, 1, 3, 3, 3, 1, 1, 0, 1, 3, 2, 0, 0, 0]
# , [1, 0, 2, 3, 3, 2, 0, 1, 2, 2, 3, 2, 3, 1, 1, 3, 2, 0, 0, 0]
# , [2, 1, 2, 1, 3, 3, 1, 2, 0, 0, 0, 2, 3, 3, 2, 1, 2, 1, 0, 0]
# , [2, 3, 0, 0, 1, 1, 2, 3, 2, 0, 0, 2, 2, 3, 2, 1, 2, 2, 0, 0]
# , [3, 3, 3, 0, 0, 2, 3, 3, 3, 2, 1, 1, 0, 1, 3, 3, 2, 2, 0, 0]
# , [0, 3, 3, 1, 2, 2, 0, 2, 3, 1, 3, 1, 0, 1, 3, 3, 2, 2, 0, 0]
# , [0, 1, 1, 2, 3, 0, 0, 0, 1, 3, 3, 3, 0, 2, 0, 1, 3, 2, 0, 0]
# , [0, 1, 3, 3, 3, 2, 0, 0, 2, 3, 3, 3, 2, 2, 0, 1, 3, 1, 0, 0]
# , [3, 2, 1, 3, 3, 3, 0, 2, 2, 0, 2, 1, 3, 3, 0, 2, 1, 1, 0, 0]
# , [1, 0, 0, 1, 2, 0, 3, 2, 0, 0, 0, 2, 3, 3, 2, 1, 2, 1, 0, 0]]

UNITED = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16e\x00\x00\x00\xaa\xaa\xa0\x00\x00\xa9\xaa\xae\x00\x00\xa9e\xab\x80\x00j\x7fa\xa0\x00\xa9Q\x7fH\x00\x9a\xb8V\xea\x00\xe0\xaf\xa0\xba\x00:A\xfdG\x80K\xe1\xae\xd7\x80\x99\xf6\x02\xf9\x90\xb0[\x82\xb9\xa0\xfc/\xe5\x1f\xa0=\xa2\xdd\x1f\xa0\x16\xc0\x7f!\xe0\x1f\xe0\xbf\xa1\xd0\xe7\xf2\x89\xf2PA\x8e\x02\xf9\x90'

UNITED_COLORS = [0x0a3194, 0x4b66a7, 0x809bd8, 0xcae0fd]

# DELTA = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0]
# , [0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0]
# , [0, 0, 0, 1, 2, 2, 2, 2, 2, 1, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0]
# , [0, 0, 0, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 0, 0]
# , [0, 0, 1, 2, 1, 1, 0, 0, 1, 1, 2, 1, 0, 0, 0, 1, 2, 2, 0, 0]
# , [0, 1, 1, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 1, 1, 0]
# , [0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0]
# , [0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0]
# , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# , [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# , [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
DELTA = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x00)\x00\x00\x00\x00j\x00\x00\x00\x01\xaa@\x00\x00\x02\xaa\x90\x00\x00\x06\xaa\xa0\x00\x00\x1a\xaa\xa4\x00\x00*\xaa\xa9\x00\x00j\xaa\xaa\x00\x01\xaa\x91\xaa@\x02\xa9\x00\x1a\x90\x06PY\x01\xa0\x14\x06\xaa\x90\x14\x00j\xaa\xa9@\x16\xaa\xaa\xaa\xa4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\xff'
DELTA_COLORS = [0xfbf3f4, 0xc67e87, 0xab1c36, 0x010200]

LUTHANSA_COLORS = [0xf2b845, 0x0b060b, 0xba965f, 0x684e32]
LUTHANSA = b'UUUUUUW\xaa\xb5UUp\x00\x0bUU\x80\x00\x00\xd5V\x00\x00\x00\xb5\\\x00\x00\x00%X\x00\x00\x00\rp\x00\x00\xaa\tc\xf8\x03_\xf9`\xbe\r\x7f\xe9`\x0bU\xff\xc9p\x02\xd6\x00\tp\x00/\x80\tX\x00\x02\xbe\r\\\x00\x00\x02%V\x00\x00\x005U\x80\x00\x00\xd5Up\x00\x0bUUW\xaa\xb5UUUUUU'

BRITISH_COLORS = [0x060406, 0xb43928, 0xb7cad3, 0x3d76a9]
BRITISH = b'\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\n\xb0\x00\x00\x00\x0e\xe0\x00\x00\x00\x03\xfc\x00\x00\x00\x00\xff\x00\x00\x00\x00\xff\xc0\x00\x00\x00?\xc0\x00\x00\x00\x00\xf0\x00\x00\x00\x02\xaa\xb0\x00\x00\x02\xa9\x00\x00\x00\x02\xa5@\x00\x00\x00\x95P\x00\x00\x00UP\x00\x00\x00\x15T\x00\x00\x00\x05U\x00\x00\x00\x05U@\x00\x00\x01UP\x00\x00\x00UP\x00\x00\x00\x00\x00'

AIR_CANADA_COLORS = [0xec3123, 0xfaf3f0, 0xf6b7b1, 0xd27069]
AIR_CANADA = b'UUiUUU[\xff\xe5UU\xbe\x96\xbeUW\xe5Y[\xd5\\U}U5bU\xc3U\xb9yU\x00Um\xb5\xb9\x00n^\xf7\x03\x00\xc0\xdf\xf5\x00\x00\x00_\xf5\xc0\x00\x03_\xb5`\x00\r^\xb5p\x00\r^}\x80\xff\x02}bji\xa9\xb9X\x95iU%V9iX\x95U\xbf\xba\xfeUUV\xf7\xe5UUUUUU'

SOUTHWEST_COLORS = [0xd93a33, 0x070707, 0xe4b493, 0x455593]
SOUTHWEST = b'UUUUUUsU}UV\x82\x8e\xaa\x95X\x00\n\xaa\xa5@\x00\x00\xaa\xa9`\x00\x00*\xa9h\x00\x00\n\xa9~\x80\x00\x00\xab\x7f\xa0\x00\x00)\x7f\xf8\x00\x00\t\x7f\xfe\x80\x00\t_\xff\xa0\x00%_\xff\xe8\x00\xb5W\xff\xfe\x80\x95U\xff\xff\xa2UU\x7f\xff\xe9UU_\xff\xf5UUW\xff\xd5UUU\x7fUUUUUUU'

ALASKA_COLORS = [0x084067, 0xeaf8f6, 0x3d7491, 0x87b3c2]
ALAKSA = b'UUUUUU_\xab\xd5UU\xf8\x00-UW\xa0\x00\x02U^\x00\x00\x08\xb5x\x008\n%\xe2\x03W\x82-\xea\x0b}`\x8d\xe8\x00\x00\xe0\x89\xc8\n\xfa\x00\t\x88=]p\t\xc8\x17\xf5`\t\xc0,=@\t\xe0*\xdf`\x8dp,\xb5\x80\x05P\x0f\x8a\x005\\\x03\x80\x00\x95W\x80\x00*UU\xe0\x02\xb5UUW\xffUU'


def get_element_from_bytes(byte_string: bytes, i: int, j: int) -> int:
    linear_index = i * ARRAY_SIZE + j
    byte_index = linear_index // 4
    element_position_in_byte = linear_index % 4
    shift = (3 - element_position_in_byte) * BITS_PER_ELEMENT
    packed_byte = byte_string[byte_index]
    shifted_value = packed_byte >> shift
    original_value = shifted_value & 0b11

    return original_value

def get_logo_g(logo, colors):
    planeBmp = displayio.Bitmap(20, 20, len(colors))
    planePalette = displayio.Palette(len(colors))

    for i in range(len(colors)):
        planePalette[i] =  colors[i]

    for i in range(20):
        for j in range(20):
            planeBmp[j, i] = get_element_from_bytes(logo, i, j)

    planeTg= displayio.TileGrid(planeBmp, pixel_shader=planePalette)
    planeTg.x = 2
    planeTg.y = 2
    planeG=displayio.Group(scale=1, x=0, y=0)
    planeG.append(planeTg)
    return planeG


