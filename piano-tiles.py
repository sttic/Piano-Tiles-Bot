from PIL import ImageGrab
import pyautogui
import time

origin, bounds = (64, 0), (64, 0, 395, 590)
tile_height = 150
threshold, compensation = 32, 128

screen = ImageGrab.grab(bounds)
x = lambda i: origin[0] + screen.width/8 + i*screen.width/4
# NOTE don't make num_sensors*step > 450
num_sensors, step = 4, 128

sensors = [tuple((x(i), origin[1] + screen.height - 150 - step*s) for i in range(4)) for s in range(num_sensors)]

while True:
    screen = ImageGrab.grab(bounds)

    for sensor in sensors:
        for i in range(len(sensor)):
            # subtract bit from sensors sample position to avoid irregular design of hold tiles
            color = screen.getpixel((sensor[i][0] - origin[0] - 25, sensor[i][1] - origin[1]))

            if next((False for channel in color if channel > threshold), True):
                # add distance to click to compensate for speed/delay
                pyautogui.click(x=sensor[i][0], y=sensor[i][1] + compensation)