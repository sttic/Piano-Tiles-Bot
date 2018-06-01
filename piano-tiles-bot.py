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
            # return rgb == (0, 1, 0)
        height = self.screen.height

        tiles = []
        for lane in range(len(sensors)):
            x = sensors[lane]
            # TODO handle if tile is at very bottom (unpausing or reviving)
            for y in range(height - speed_compensation, color_gap, -1):
                color = self.screen.getpixel((x, y))
                color_below = self.screen.getpixel((x, y + 1))
                color_fill = self.screen.getpixel((x, y - color_gap))

                if is_black(color) and not is_black(color_below) and is_black(color_fill):
                    tiles.append(Tile(lane, y))
        return tiles

class Tile:
    def __init__(self, lane, y, varient='short'):
        self.lane = lane
        self.x = sensors[lane]
        self.y = y
        self.varient = varient

def click(x, y):
    pyautogui.click(x=x + origin[0], y=y + origin[1] + speed_compensation, clicks=num_clicks)

bounds = (64, 0, 395, 590)
origin, screen_width, screen_height = bounds[:2], bounds[2] - bounds[0], bounds[3] - bounds[1]
tile_height, num_lanes = 150, 4
threshold, speed_compensation = 3, 52
color_gap, num_clicks = 16, 3

x = lambda i: screen_width/(2*num_lanes) + i*screen_width/num_lanes
sensors = [x(i) for i in range(num_lanes)]

while True:
    current_screen = Screen(bounds)
    current_tiles = current_screen.read()
    current_tiles.sort(key=lambda tile: tile.y, reverse=True)
    count = 0

    for tile in current_tiles:
        click(tile.x, tile.y)
        count += 1
        if count >= 2:
            break
