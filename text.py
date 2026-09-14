import constants
from adafruit_display_text.label import Label
import displayio

def make_text_labels(display):
    font = constants.font
    ROW_ONE_COLOUR=constants.ROW_ONE_COLOUR
    ROW_TWO_COLOUR=constants.ROW_TWO_COLOUR
    ROW_THREE_COLOUR=constants.ROW_THREE_COLOUR
    
    label1 = Label(
        font,
        color=ROW_ONE_COLOUR,
        text=constants.label1_short)
    bbx, bby, bbwidth, bbh = label1.bounding_box
    label1.x = round((display.width + 24) / 2 - bbwidth / 2)
    label1.y = display.height // 6

    label2 = Label(
        font,
        color=ROW_TWO_COLOUR,
        text=constants.label3_short)
    bbx, bby, bbwidth, bbh = label2.bounding_box
    label2.x = round((display.width + 24) / 2 - bbwidth / 2)
    label2.y = display.height // 6 * 3

    label3 = Label(
        font,
        color=ROW_THREE_COLOUR,
        text=constants.label2_short)
    bbx, bby, bbwidth, bbh = label3.bounding_box
    label3.x = round(display.width / 2 - bbwidth / 2)
    label3.y = display.height // 6 * 5 - 1

    return label1, label2, label3

def make_position_marker(display):
    pal = displayio.Palette(2)
    pal[0] = 0x000000
    pal[1] = 0xFF0000

    half = constants.VIEW_FOV_DEG / 2.0
    off = constants.plane_off_deg
    if off < -half:
        off = -half
    if off > half:
        off = half
    x = int((off + half) / constants.VIEW_FOV_DEG * (display.width - 2))

    sprite = displayio.Bitmap(2, 2, 2)
    sprite[0, 0] = 1
    sprite[1, 0] = 1
    sprite[0, 1] = 1
    sprite[1, 1] = 1
    tg = displayio.TileGrid(sprite, pixel_shader=pal)
    tg.x = x
    tg.y = display.height - 2
    return tg


def print_label_contents():
    print("printing labels!")
    print("1")
    print(constants.label1_short)
    print("2")
    print(constants.label2_short)
    print("3")
    print(constants.label3_short)
