from hardware import RGB_LED
from random import randint
from time import sleep


class RGB_Control:
    """RGB control via Adafruit NeoPixel object RGB_LED defined in hardware.py"""

    def __init__(self):
        self.RGB_LED = RGB_LED

    COLOR = {
        "Red": (255, 0, 0),
        "Green": (0, 255, 0),
        "Blue": (0, 0, 255),
        "Off": (0, 0, 0),
    }

    def solid(self, color):
        """Set the LED to a solid color"""
        self.RGB_LED.fill(self.COLOR[color])
        self.RGB_LED.show()

    def chase(self, color, delay):
        """Chase the LED with a specific color and delay"""
        for i in range(self.RGB_LED.n):
            self.RGB_LED[i] = self.COLOR[color]
            sleep(delay)
            self.RGB_LED.show()

    def chase_off_on(self, color, delay):
        """Chase from off to the selected color"""
        for i in range(self.RGB_LED.n):
            self.RGB_LED[i] = self.COLOR["Off"]
            sleep(delay)
            self.RGB_LED.show()
        for i in range(self.RGB_LED.n):
            self.RGB_LED[i] = self.COLOR[color]
            sleep(delay)
            self.RGB_LED.show()

    def chase_on_off(self, color, delay):
        """Chase from the selected color to off"""
        for i in range(self.RGB_LED.n):
            self.RGB_LED[i] = self.COLOR[color]
            sleep(delay)
            self.RGB_LED.show()
        for i in range(self.RGB_LED.n):
            self.RGB_LED[i] = self.COLOR["Off"]
            sleep(delay)
            self.RGB_LED.show()

    def single_blink(self, color, delay):
        """Blink a single LED at a time"""
        for i in range(self.RGB_LED.n):
            self.RGB_LED[i] = self.COLOR[color]
            self.RGB_LED.show()
            sleep(delay)
            self.RGB_LED[i] = self.COLOR["Off"]
            self.RGB_LED.show()
            sleep(delay)

    def all_blink(self, color, delay):
        """Blink all LEDs simultaneously"""
        self.RGB_LED.fill(self.COLOR[color])
        self.RGB_LED.show()
        sleep(delay)
        self.RGB_LED.fill(self.COLOR["Off"])
        self.RGB_LED.show()
        sleep(delay)


class RGB_Settings:
    """Class to hold and update RGB setting state"""

    def __init__(self):
        self.color = "Off"
        self.pattern = "chase"
        self.delay = 0.005
        self.repeat = 1

    def state(self):
        state = {
            "color": self.color,
            "pattern": self.pattern,
            "delay": self.delay,
            "repeat": self.repeat,
        }
        return state

    def update(self, color="Off", pattern="chase", delay=0.005, repeat=1):
        """Update the RGB settings"""
        self.color = color
        self.pattern = pattern
        self.delay = delay
        self.repeat = repeat
