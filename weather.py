import constants
from adafruit_display_text.label import Label
import displayio

# def make_plane(big_plane=False):
#     planeBmp = displayio.Bitmap(12, 12, 2)
#     planePalette = displayio.Palette(2)
#     planePalette[1] = 0xEE82EE
#     planePalette[0] = 0x000000
#     planeBmp[6,0]=planeBmp[6,1]=planeBmp[5,1]=planeBmp[4,2]=planeBmp[5,2]=planeBmp[6,2]=1
#     planeBmp[9,3]=planeBmp[5,3]=planeBmp[4,3]=planeBmp[3,3]=1
#     planeBmp[1,4]=planeBmp[2,4]=planeBmp[3,4]=planeBmp[4,4]=planeBmp[5,4]=planeBmp[6,4]=planeBmp[7,4]=planeBmp[8,4]=planeBmp[9,4]=1
#     planeBmp[1,5]=planeBmp[2,5]=planeBmp[3,5]=planeBmp[4,5]=planeBmp[5,5]=planeBmp[6,5]=planeBmp[7,5]=planeBmp[8,5]=planeBmp[9,5]=1
#     planeBmp[9,6]=planeBmp[5,6]=planeBmp[4,6]=planeBmp[3,6]=1
#     planeBmp[6,9]=planeBmp[6,8]=planeBmp[5,8]=planeBmp[4,7]=planeBmp[5,7]=planeBmp[6,7]=1

#     planeFlipped = flip_plane(planeBmp)

#     planeTg= displayio.TileGrid(planeFlipped, pixel_shader=planePalette)
#     planeG=displayio.Group(scale=1, x=0, y=10)
#     planeG.append(planeTg)
#     return planeG


SUNSET = [
    # Row 0 (Sky)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 1 (Outer Rays)
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    # Row 2 (Central Ray)
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 3 (Mid Rays)
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    # Row 4 (Inner Rays)
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    # Row 5 (Top of Sun - 3 pixels wide)
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    # Row 6 (Base of Sun - 5 pixels wide)
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    # Row 7 (Horizon Line)
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

def show_weather(display):
    font = constants.font
    ROW_ONE_COLOUR=constants.ROW_ONE_COLOUR
    ROW_TWO_COLOUR=constants.ROW_TWO_COLOUR
    ROW_THREE_COLOUR=constants.ROW_THREE_COLOUR
    
    high = Label(
        font,
        color=ROW_ONE_COLOUR,
        text="77")
    bbx, bby, bbwidth, bbh = high.bounding_box
    high.x = round(24 + (19 - bbwidth) // 2)
    high.y = display.height // 6 + 1 

    dotBmp = displayio.Bitmap(1, 1, 1)
    dotPalette = displayio.Palette(1)
    dotPalette[0] = ROW_ONE_COLOUR
    dotTg = displayio.TileGrid(dotBmp, pixel_shader=dotPalette)
    dotTg.x = high.x + bbwidth
    dotTg. y = 2


    low = Label(
        font,
        color=ROW_ONE_COLOUR,
        text="56")
    bbx, bby, bbwidth, bbh = low.bounding_box
    low.x = round(43 + (19 - bbwidth) // 2)
    print("width: ", display.width, "bbwidth ", bbwidth, "x ", low.x)
    low.y = display.height // 6 + 1 

    dotBmp = displayio.Bitmap(1, 1, 1)
    dotPalette = displayio.Palette(1)
    dotPalette[0] = ROW_ONE_COLOUR
    dotTg2 = displayio.TileGrid(dotBmp, pixel_shader=dotPalette)
    dotTg2.x = low.x + bbwidth
    dotTg2. y = 2
    
    time = Label(
        font,
        color=ROW_TWO_COLOUR,
        text="5:30")
    bbx, bby, bbwidth, bbh = time.bounding_box
    time.x = round(40)
    time.y = display.height // 6 * 3 + 1
    print("time width ", bbwidth)
    
    label3 = Label(
        font,
        color=ROW_THREE_COLOUR,
        text="<list of future weather>")
    bbx, bby, bbwidth, bbh = label3.bounding_box
    label3.x = round(display.width / 2 - bbwidth / 2)
    label3.y = display.height // 6 * 5 + 2

    sunBmp = displayio.Bitmap(18, 8, 3)
    sunPalette = displayio.Palette(3)
    sunPalette[0] = 0x000000
    sunPalette[1] = 0xFCD34D
    sunPalette[2] = 0x4B5563

    for i in range(8):
        for j in range(18):
            sunBmp[j, i] = SUNSET[i][j]

    sunTg = displayio.TileGrid(sunBmp, pixel_shader=sunPalette)
    sunTg.x = 20
    sunTg.y = display.height // 6 * 3 + 1

    return high, low, time, label3, dotTg, dotTg2, sunTg
