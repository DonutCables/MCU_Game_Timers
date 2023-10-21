"""
Hardware declarations for the timer project.
Used to easily change pin connections without changing the primary code.
"""
from machine import Pin, I2C, UART
from rotary_irq_rp2 import RotaryIRQ
from neopixel import NeoPixel
from adafruit_debouncer import Button
from lcd_i2c8574_m import I2cLcd
from utime import ticks_ms


class DisplayWrapper:
    """Wrapper for I2C LCD display"""

    def __init__(
        self,
        sda_pin=0,
        scl_pin=1,
        lcd_addresses=[0x27, 0x3F],
        rows=2,
        cols=16,
    ):
        self.i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.display = None
        self.lcd_addresses = lcd_addresses
        self.dimensions = (cols, rows)
        self.init_lcd()

    def init_lcd(self):
        for addr in self.lcd_addresses:
            try:
                self.display = I2cLcd(self.i2c, addr, self.dimensions)
            except Exception:
                continue
            else:
                return

    def write(self, text):
        if self.display is not None:
            self.display.write(text)

    def clear(self):
        if self.display is not None:
            self.display.clear()


class Encoder_Wrapper:
    def __init__(self, pin_a, pin_b):
        self.encoder = RotaryIRQ(
            pin_num_clk=pin_a, pin_num_dt=pin_b, reverse=True, pull_up=True
        )
        self._value = 0

    @property
    def position(self):
        return self.encoder.value()


class Button_Wrapper:
    def __init__(self, pin):
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._value = False

    @property
    def value(self):
        self._value = self.button.value()
        return self._value


class LED_Wrapper:
    """Wrapping pin LED functionality"""

    def __init__(self, pin_number):
        self.pin = Pin(pin_number, Pin.OUT)
        self._value = False  # Private variable to store the LED state
        self._prev_value = False  # Private variable to track the previous LED state

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value != self._value:
            self._value = new_value
            if new_value:
                self.pin.high()
            else:
                self.pin.low()


DISPLAY = DisplayWrapper(0, 1, [0x27, 0x3F], 2, 16)

# UART audio output
AUDIO_OUT = UART(1, tx=Pin(4), rx=Pin(5), baudrate=9600)

# Initialize RGB and inputs
iopins = (
    26,  # RGB data pin
    8,  # Encoder pin 1
    7,  # Encoder pin 2
    6,  # Encoder button
    17,  # Red button
    14,  # Blue button
    16,  # Red LED
    15,  # Blue LED
)

# RGB strip setup
led_count = 58
RGB_LED = NeoPixel(Pin(iopins[0]), led_count)

# Encoder rotary setup
ENCODER = Encoder_Wrapper(pin_a=8, pin_b=7)

# Setup button DIO objects
ENC, RED, BLUE = (Button_Wrapper(pin) for pin in iopins[3:6])


# Create debouncer objects from DIO buttons
hold_ms = 2000
ENCB, REDB, BLUEB = (
    Button(ENC, long_duration_ms=hold_ms),
    Button(RED, long_duration_ms=hold_ms),
    Button(BLUE, long_duration_ms=hold_ms),
)

# Team button LED setup
RED_LED, BLUE_LED = (LED_Wrapper(pin) for pin in iopins[6:8])


def monotonic():
    """Converts uPython ticks_ms to CirPy monotonic time"""
    return ticks_ms() / 1000
