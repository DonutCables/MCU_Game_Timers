"""
Hardware declarations for the timer project.
Used to easily change pin connections without changing the primary code.
"""
import board
from busio import I2C, UART
from digitalio import DigitalInOut, Pull
from rotaryio import IncrementalEncoder
from adafruit_debouncer import Button  # type: ignore
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
                    print("trying", addr)
                    self.display = I2cLcd(self.i2c, addr, self.dimensions)
                except Exception:
                    print("failed", addr)
                    continue
                else:
                    print("success", addr)
                    return

    def write(self, text):
        if self.display is not None:
            self.display.write(text)

    def clear(self):
        if self.display is not None:
            self.display.clear()


# UART audio output
try:
    AUDIO_OUT = UART(board.GPIO1, board.GPIO2, baudrate=9600)
except Exception:
    print("AUDIO_OUT failed")
    pass

# I2C display creation
try:
    DISPLAY = DisplayWrapper(board.GPIO41, board.GPIO42, rows=2, cols=16)
except Exception:
    print("DISPLAY failed")
    pass


# Initialize RGB and inputs
iopins = (
    board.GPIO40,  # RGB data pin
    board.GPIO14,  # Encoder pin 1
    board.GPIO13,  # Encoder pin 2
    board.GPIO12,  # Encoder button
    board.GPIO7,  # Red button
    board.GPIO4,  # Blue button
    board.GPIO6,  # Red LED
    board.GPIO5,  # Blue LED
)


# Encoder rotary setup
try:
    ENCODER = IncrementalEncoder(iopins[1], iopins[2])
except Exception:
    print("ENCODER failed")
    pass

# Setup button DIO objects
try:
    ENC = DigitalInOut(iopins[3])
    ENC.switch_to_input(Pull.UP)
except Exception:
    print("BUTTONS failed")
    pass

# Create debouncer objects from DIO buttons
hold_ms = 1000
try:
    ENCB = Button(ENC, long_duration_ms=hold_ms * 2)
except Exception:
    print("DEBOUNCERS failed")
    pass
