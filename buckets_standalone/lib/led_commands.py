"""
Layer for cleaner control of RGB output
"""
from hardware import RGB_LED
from time import sleep


COLOR = {
    "Red": (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue": (0, 0, 255),
    "Off": (0, 0, 0),
}


def rgb_control(color="Off", pattern="chase", delay=0.005):
    """RGB control via Adafruit NeoPixel"""
    global RGB_LED
    if pattern == "solid":
        RGB_LED.fill(COLOR[color])
        RGB_LED.show()
    elif pattern == "chase":
        for i in range(RGB_LED.n):
            RGB_LED[i] = COLOR[color]
            sleep(delay)
            RGB_LED.show()
    elif pattern == "single_blink":
        for i in range(RGB_LED.n):
            RGB_LED[i] = COLOR[color]
            RGB_LED.show()
            sleep(delay)
            RGB_LED[i] = COLOR["off"]
            RGB_LED.show()
            sleep(delay)
    elif pattern == "all_blink":
        RGB_LED.fill(COLOR[color])
        RGB_LED.show()
        sleep(delay)
        RGB_LED.fill(COLOR["off"])
        RGB_LED.show()
        sleep(delay)
    print(color, pattern)
