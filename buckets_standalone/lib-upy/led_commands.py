# Add the line level suppression for pyline general type issues
import uasyncio
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

    async def solid(self, color, delay):
        """Set the LED to a solid color"""
        self.RGB_LED.fill(self.COLOR[color])
        self.RGB_LED.write()

    async def chase(self, color, delay):
        """Chase the LED with a specific color and delay"""
        for i in range(self.RGB_LED.__len__()):
            self.RGB_LED[i] = self.COLOR[color]
            await uasyncio.sleep(delay)
            self.RGB_LED.write()

    async def chase_off_on(self, color, delay):
        """Chase from off to the selected color"""
        await self.chase("Off", delay)
        await self.chase(color, delay)

    async def chase_on_off(self, color, delay):
        """Chase from the selected color to off"""
        await self.chase(color, delay)
        await self.chase("Off", delay)

    async def single_blink_on_off(self, color, delay):
        """Blink a single LED on at a time"""
        for i in range(self.RGB_LED.__len__()):
            self.RGB_LED[i] = self.COLOR[color]
            self.RGB_LED.write()
            await uasyncio.sleep(delay)
            self.RGB_LED[i] = self.COLOR["Off"]
            self.RGB_LED.write()
            await uasyncio.sleep(delay)

    async def single_blink_off_on(self, color, delay):
        """Blink a single LED off at a time"""
        for i in range(self.RGB_LED.__len__()):
            self.RGB_LED[i] = self.COLOR["Off"]
            self.RGB_LED.write()
            await uasyncio.sleep(delay)
            self.RGB_LED[i] = self.COLOR[color]
            self.RGB_LED.write()
            await uasyncio.sleep(delay)

    async def all_blink(self, color, delay):
        """Blink all LEDs simultaneously"""
        self.RGB_LED.fill(self.COLOR[color])
        self.RGB_LED.write()
        await uasyncio.sleep(delay)
        self.RGB_LED.fill(self.COLOR["Off"])
        self.RGB_LED.write()
        await uasyncio.sleep(delay)


class RGB_Settings:
    """Class to hold and update RGB setting state"""

    def __init__(self):
        self.color = "Off"
        self.pattern = "chase"
        self.delay = 0.005
        self.repeat = 0
        self.hold = False

    def state(self):
        return {
            "color": self.color,
            "pattern": self.pattern,
            "delay": self.delay,
            "repeat": self.repeat,
            "hold": self.hold,
        }

    def update(self, color="Off", pattern="chase", delay=0.005, repeat=1, hold=False):
        """Update the RGB settings"""
        self.color = color
        self.pattern = pattern
        self.delay = delay
        self.repeat = repeat
        self.hold = hold
