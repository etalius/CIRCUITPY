import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label


def update_time(hours, minutes, display):
    group = displayio.Group() 
    color = displayio.Palette(1)
    color[0] = 0xFFFFFF

    # Set font and color
    clock_font = bitmap_font.load_font("IBMPlexMono-Medium-24_jep.bdf")
    clock_label = Label(clock_font)
    clock_label.color = color[0]

    # Do math for 24h to 12h time
    if hours > 12:  # Handle times later than 12:59
        hours -= 12
    elif not hours:  # Handle times between 0:00 and 0:59
        hours = 12

    # Set the text
    colon = ":"
    clock_label.text = "{hours}{colon}{minutes:02d}".format(
        hours=hours, minutes=minutes, colon=colon
    )
    # Center the label
    _, _, bbwidth, _ = clock_label.bounding_box
    clock_label.x = round(display.width / 2 - bbwidth / 2)
    clock_label.y = display.height // 2
    group.append(clock_label)
    display.root_group = group