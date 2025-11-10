import constants
from adafruit_display_text.label import Label

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
    label1.x = round((display.width  + 24) / 2 - bbwidth / 2)
    label1.y = display.height // 6 + 1 
    
    
    label2 = Label(
        font,
        color=ROW_TWO_COLOUR,
        text=constants.label3_short)
    bbx, bby, bbwidth, bbh = label2.bounding_box
    label2.x = round((display.width + 24)  / 2 - bbwidth / 2)
    label2.y = display.height // 6 * 3 + 1
    
    label3 = Label(
        font,
        color=ROW_THREE_COLOUR,
        text=constants.label2_short)
    bbx, bby, bbwidth, bbh = label3.bounding_box
    label3.x = round(display.width / 2 - bbwidth / 2)
    label3.y = display.height // 6 * 5 + 2

    return label1, label2, label3

def print_label_contents():
    print("printing labels!")
    print("1")
    print(constants.label1_short)
    print("2")
    print(constants.label2_short)
    print("3")
    print(constants.label3_short)
