
import displayio

def scale_plane(input_array, new_shape):
    rows_in = 12
    cols_in = 12
    rows_out, cols_out = new_shape

    planeBmpNew = displayio.Bitmap(new_shape[0], new_shape[1], 2)

    row_scale = rows_in / rows_out
    col_scale = cols_in / cols_out

    for row_out in range(rows_out):
        for col_out in range(cols_out):
            row_in = int(row_out * row_scale)
            col_in = int(col_out * col_scale)

            # Nearest-neighbor interpolation: take the closest pixel
            row_in = min(rows_in - 1, max(0, row_in)) #Clamping for edge cases.
            col_in = min(cols_in - 1, max(0, col_in)) #Clamping for edge cases.

            planeBmpNew[row_out, col_out] = input_array[row_in, col_in]

    return planeBmpNew

def flip_plane(array):
    rows = 12
    cols = 12
    planeBmpNew = displayio.Bitmap(12, 12, 2)  # Create a new array

    for i in range(rows):
        for j in range(cols):
            planeBmpNew[rows - 1 - i, j] = array[i, j]

    return planeBmpNew

# Little plane to scroll across when we find a flight overhead
def make_plane(big_plane=False):
    planeBmp = displayio.Bitmap(12, 12, 2)
    planePalette = displayio.Palette(2)
    planePalette[1] = 0xEE82EE
    planePalette[0] = 0x000000
    planeBmp[6,0]=planeBmp[6,1]=planeBmp[5,1]=planeBmp[4,2]=planeBmp[5,2]=planeBmp[6,2]=1
    planeBmp[9,3]=planeBmp[5,3]=planeBmp[4,3]=planeBmp[3,3]=1
    planeBmp[1,4]=planeBmp[2,4]=planeBmp[3,4]=planeBmp[4,4]=planeBmp[5,4]=planeBmp[6,4]=planeBmp[7,4]=planeBmp[8,4]=planeBmp[9,4]=1
    planeBmp[1,5]=planeBmp[2,5]=planeBmp[3,5]=planeBmp[4,5]=planeBmp[5,5]=planeBmp[6,5]=planeBmp[7,5]=planeBmp[8,5]=planeBmp[9,5]=1
    planeBmp[9,6]=planeBmp[5,6]=planeBmp[4,6]=planeBmp[3,6]=1
    planeBmp[6,9]=planeBmp[6,8]=planeBmp[5,8]=planeBmp[4,7]=planeBmp[5,7]=planeBmp[6,7]=1

    planeFlipped = flip_plane(planeBmp)

    planeTg= displayio.TileGrid(planeFlipped, pixel_shader=planePalette)
    planeG=displayio.Group(scale=1, x=0, y=10)
    planeG.append(planeTg)
    return planeG

def make_plane_for_logo():
    planeBmp = displayio.Bitmap(12, 12, 2)
    planePalette = displayio.Palette(2)
    planePalette[1] = 0xEE82EE
    planePalette[0] = 0x000000
    planeBmp[6,0]=planeBmp[6,1]=planeBmp[5,1]=planeBmp[4,2]=planeBmp[5,2]=planeBmp[6,2]=1
    planeBmp[9,3]=planeBmp[5,3]=planeBmp[4,3]=planeBmp[3,3]=1
    planeBmp[1,4]=planeBmp[2,4]=planeBmp[3,4]=planeBmp[4,4]=planeBmp[5,4]=planeBmp[6,4]=planeBmp[7,4]=planeBmp[8,4]=planeBmp[9,4]=1
    planeBmp[1,5]=planeBmp[2,5]=planeBmp[3,5]=planeBmp[4,5]=planeBmp[5,5]=planeBmp[6,5]=planeBmp[7,5]=planeBmp[8,5]=planeBmp[9,5]=1
    planeBmp[9,6]=planeBmp[5,6]=planeBmp[4,6]=planeBmp[3,6]=1
    planeBmp[6,9]=planeBmp[6,8]=planeBmp[5,8]=planeBmp[4,7]=planeBmp[5,7]=planeBmp[6,7]=1

    # planeBmpNew = scale_plane(planeBmp, (20, 20))
    planeTg= displayio.TileGrid(planeBmp, pixel_shader=planePalette)
    planeTg.x = 9
    planeTg.y = 6
    planeG=displayio.Group(scale=1, x=0, y=0)
    planeG.append(planeTg)
    return planeG