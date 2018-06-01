from PIL import ImageGrab
import pyautogui
import time

class Screen:
    def __init__(self, bounds):
        self.screen = ImageGrab.grab(bounds)
        self.time = time.time()

    def read(self):
        def is_black(rgb):
            return next((False for channel in rgb if channel > threshold), True)
        height = self.screen.height

        tiles = [[] for i in range(num_lanes)]
        for lane in range(len(sensors)):
            x = sensors[lane]
            # TODO handle if tile is at very bottom (unpausing or reviving)
            for y in range(height - tile_height//2, 0, -1):
                color = self.screen.getpixel((x, y))
                color_below = self.screen.getpixel((x, y + 1))
                if is_black(color) and not is_black(color_below):
                    tiles[lane].append(Tile(lane, y))
        return tiles

class Tile:
    def __init__(self, lane, y, varient='short'):
        self.lane = lane
        self.x = sensors[lane]
        self.y = y
        self.varient = varient

def click(x, y):
    pyautogui.click(x=x + origin[0], y=y + origin[1] + speed_compensation)

bounds = (64, 0, 395, 590)
origin, screen_width, screen_height = bounds[:2], bounds[2] - bounds[0], bounds[3] - bounds[1]
tile_height, num_lanes = 150, 4
threshold, speed_compensation = 4, 90

x = lambda i: screen_width/8 + i*screen_width/4
sensors = [x(i) for i in range(num_lanes)]

past_screen = Screen(bounds)
past_tiles = past_screen.read()

max_clicks = 1

while True:
    current_screen = Screen(bounds)
    current_tiles = current_screen.read()

    for lane in current_tiles:
        for tile in lane:
            click(tile.x, tile.y)

# 1858