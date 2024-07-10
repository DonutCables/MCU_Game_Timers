"""
Customized LED commands for RGB strip via Adafruit NeoPixel.
"""
from asyncio import sleep
from neopixel import NeoPixel


class RGB_Control:
    """RGB control via Adafruit NeoPixel object"""

    def __init__(self, rgb: NeoPixel):
        self.rgb = rgb

    COLOR = {
        "Red": (255, 0, 0),
        "Orange": (255, 165, 0),
        "Yellow": (255, 255, 0),
        "Green": (0, 255, 0),
        "Blue": (0, 0, 255),
        "Purple": (255, 0, 255),
        "Off": (0, 0, 0),
    }

    async def solid(self, color, delay):
        """Set the LED to a solid color"""
        self.rgb.fill(self.COLOR[color])
        self.rgb.show()

    async def chase(self, color, delay):
        """Chase the LED with a specific color and delay"""
        for i in range(self.rgb.n):
            self.rgb[i] = self.COLOR[color]
            await sleep(delay)
            self.rgb.show()
            await sleep(0)

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
        for i in range(self.rgb.n):
            self.rgb[i] = self.COLOR[color]
            self.rgb.show()
            await sleep(delay)
            self.rgb[i] = self.COLOR["Off"]
            self.rgb.show()
            await sleep(delay)

    async def single_blink_off_on(self, color, delay):
        """Blink a single LED off at a time"""
        for i in range(self.rgb.n):
            self.rgb[i] = self.COLOR["Off"]
            self.rgb.show()
            await sleep(delay)
            self.rgb[i] = self.COLOR[color]
            self.rgb.show()
            await sleep(delay)

    async def all_blink(self, color, delay):
        """Blink all LEDs simultaneously"""
        self.rgb.fill(self.COLOR[color])
        self.rgb.show()
        await sleep(delay)
        self.rgb.fill(self.COLOR["Off"])
        self.rgb.show()
        await sleep(delay)


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

    async def rgb_control(self, rgb):
        """Async function for controlling RGB LEDs"""
        while True:
            if self.repeat > 0 or self.repeat == -1:
                pattern = getattr(rgb, self.pattern, "chase")
                if callable(pattern):
                    await pattern(self.color, self.delay)
                if self.repeat > 0:
                    self.repeat -= 1
                    if self.repeat == 0:
                        self.hold = False
            await sleep(0)
