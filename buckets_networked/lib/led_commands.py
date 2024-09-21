"""
Customized LED commands for RGB strip via Adafruit NeoPixel.
"""
from asyncio import sleep
from neopixel import NeoPixel


class RGB_Control:
    """RGB control via Adafruit NeoPixel object"""

    def __init__(self, rgb: NeoPixel):
        self.rgb = rgb
        self.loop = False

    COLOR = {
        "Red": (255, 0, 0),
        "Orange": (255, 165, 0),
        "Yellow": (255, 255, 0),
        "Green": (0, 255, 0),
        "Blue": (0, 0, 255),
        "Purple": (255, 0, 255),
        "White": (255, 255, 255),
        "Off": (0, 0, 0),
    }

    def stop(self):
        """Stop the RGB loop"""
        self.loop = False

    def start(self):
        """Start the RGB loop"""
        self.loop = True

    async def solid(self, color1, color2, delay):
        """Set the LED to a solid color"""
        self.rgb.fill(self.COLOR[color1])
        self.rgb.show()

    async def fill(self, color1, color2, delay):
        """Fill the LED with a specific color and delay"""
        for i in range(self.rgb.n):
            self.rgb[i] = self.COLOR[color1]
            self.rgb.show()
            await sleep(delay)
            await sleep(0)
            if not self.loop:
                break

    async def fill_cycle(self, color1, color2, delay):
        """Fill one color then the other"""
        await self.fill(color1, color2, delay)
        await self.fill(color2, color1, delay)

    async def single_blink_cycle(self, color1, color2, delay):
        """Blink a single LED on at a time"""
        for i in range(self.rgb.n):
            self.rgb[i] = self.COLOR[color1]
            self.rgb.show()
            await sleep(delay)
            self.rgb[i] = self.COLOR[color2]
            self.rgb.show()
            await sleep(delay)
            if not self.loop:
                break

    async def solid_blink(self, color1, color2, delay):
        """Blink all LEDs simultaneously, up to two colors"""
        await self.solid(color1, color2, delay)
        await sleep(delay)
        await self.solid(color2, color1, delay)
        await sleep(delay)


class RGB_Settings:
    """Class to hold and update RGB setting state"""

    def __init__(self, rgb):
        self.color1 = "Off"
        self.color2 = "Off"
        self.pattern = "fill"
        self.delay = 0.005
        self.repeat = 0
        self.hold = False
        self.rgb = rgb

    def state(self):
        return {
            "color1": self.color1,
            "color2": self.color2,
            "pattern": self.pattern,
            "delay": self.delay,
            "repeat": self.repeat,
            "hold": self.hold,
            "rgb": self.rgb,
        }

    def update(
        self,
        color1="Off",
        color2="Off",
        pattern="fill",
        delay=0.005,
        repeat=1,
        hold=False,
    ):
        """Update the RGB settings"""
        self.rgb.stop()
        self.color1 = color1
        self.color2 = color2
        self.pattern = pattern
        self.delay = delay
        self.repeat = repeat
        self.hold = hold

    async def rgb_control(self, rgb):
        """Async function for controlling RGB LEDs"""
        while True:
            while self.repeat == -1:
                self.rgb.start()
                pattern = getattr(rgb, self.pattern, "fill")
                if callable(pattern):
                    await pattern(self.color1, self.color2, self.delay)
                self.rgb.stop()
                await sleep(0)
            while self.repeat > 0:
                self.rgb.start()
                self.repeat -= 1
                pattern = getattr(rgb, self.pattern, "fill")
                if callable(pattern):
                    await pattern(self.color1, self.color2, self.delay)
                self.rgb.stop()
                if self.repeat == 0:
                    self.hold = False
                await sleep(0)
            await sleep(0)
