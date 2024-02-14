# type: ignore
"""
Hardware declarations for the timer project.
Used to easily change pin connections without changing the primary code.
This file is for the Timerbox component.
"""
import board
from busio import I2C
from digitalio import DigitalInOut, Pull, DriveMode
from rotaryio import IncrementalEncoder
from adafruit_debouncer import Button
from lcd_i2c8574_m import I2cLcd


class DisplayWrapper:
    """Wrapper for I2C LCD display"""

    def __init__(
        self,
        sda_pin,
        scl_pin,
        lcd_addresses=[0x27, 0x3F],
        rows=2,
        cols=16,
    ):
        self.i2c = I2C(scl_pin, sda_pin)
        self.display = None
        self.lcd_addresses = lcd_addresses
        self.dimensions = (cols, rows)
        self.init_lcd()

    def init_lcd(self):
        while self.i2c.try_lock():
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


# I2C display creation
try:
    DISPLAY = DisplayWrapper(board.IO5, board.IO6, rows=2, cols=16)
except Exception as e:
    print("DISPLAY failed")
    print(e)
    pass


# Group IO pins
iopins = (
    board.IO10,  # RGB data pin
    board.IO9,  # Encoder pin 1
    board.IO8,  # Encoder pin 2
    board.IO7,  # Encoder button
    board.IO1,  # Red button
    board.IO3,  # Blue button
    board.IO2,  # Red LED
    board.IO4,  # Blue LED
)

# Encoder rotary setup
try:
    ENCODER = IncrementalEncoder(iopins[1], iopins[2])
except Exception as e:
    print("ENCODER failed")
    print(e)
    pass

# Setup button DIO objects
try:
    ENC = DigitalInOut(iopins[3])
    ENC.switch_to_input(Pull.UP)
except Exception as e:
    print("BUTTONS failed")
    print(e)
    pass

# Create debouncer objects from DIO buttons
hold_ms = 1000
try:
    ENCB = Button(ENC, long_duration_ms=hold_ms * 2)
except Exception as e:
    print("DEBOUNCERS failed")
    print(e)
    pass
