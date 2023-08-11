import board
import busio
import rotaryio
import digitalio
import neopixel

from lcd import LCD 
from i2c_pcf8574_interface import I2CPCF8574Interface

# I2C display assignments
lcd_i2c = busio.I2C(board.GP1, board.GP0)
pcf_interface = I2CPCF8574Interface(lcd_i2c, 0x27)
DISPLAY = LCD(pcf_interface, num_rows=2, num_cols=16)

# Initialize rotary encoder and buttons
iopins = (board.GP26_A0, board.GP8, board.GP7, board.GP6, board.GP16, board.GP17, board.GP15, board.GP14)

led_count = 58
RGB_LED = neopixel.NeoPixel(iopins[0], led_count, brightness=0.3, auto_write=False)

ENCODER = rotaryio.IncrementalEncoder(iopins[1], iopins[2])
ENC, RED_LED, RED, BLUE_LED, BLUE = (digitalio.DigitalInOut(pin) for pin in iopins[3:])
for button in [ENC, RED, BLUE]:
    button.switch_to_input(digitalio.Pull.UP)
for led in [RED_LED, BLUE_LED]:
    led.switch_to_output(False, digitalio.DriveMode.PUSH_PULL)
