from PIL import ImageGrab
import pyautogui

bounds = (64, 0, 395, 590)
origin, screen_width, screen_height = bounds[:2], bounds[2] - bounds[0], bounds[3] - bounds[1]
tile_height = 150
threshold, sensor_offset, speed_compensation = 32, 25, 112

x = lambda i: origin[0] + screen_width/8 + i*screen_width/4
num_sensors, step = 4, 128
assert num_sensors*step < screen_height

sensors = [tuple((x(i), origin[1] + screen_height - tile_height - step*s) for i in range(4)) for s in range(num_sensors)]

while True:
    screen = ImageGrab.grab(bounds)

    for sensor in sensors:
        for i in range(len(sensor)):
            color = screen.getpixel((sensor[i][0] - origin[0] - sensor_offset, sensor[i][1] - origin[1]))
            if next((False for channel in color if channel > threshold), True):
                pyautogui.click(x=sensor[i][0], y=sensor[i][1] + speed_compensation)
