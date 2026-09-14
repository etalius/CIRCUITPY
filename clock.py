import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
import gc


def update_time(hours, minutes, display):
    group = displayio.Group()
    color = displayio.Palette(1)
    color[0] = 0xFFFFFF

    clock_font = bitmap_font.load_font("IBMPlexMono-Medium-24_jep.bdf")
    clock_label = Label(clock_font)
    clock_label.color = color[0]

    if hours > 12:
        hours -= 12
    elif not hours:
        hours = 12

    clock_label.text = "{hours}:{minutes:02d}".format(hours=hours, minutes=minutes)
    gc.collect()
    _, _, bbwidth, _ = clock_label.bounding_box
    clock_label.x = round(display.width / 2 - bbwidth / 2)
    clock_label.y = display.height // 2
    group.append(clock_label)
    display.root_group = group
