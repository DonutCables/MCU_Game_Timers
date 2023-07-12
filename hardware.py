import board
import busio
import rotaryio
import digitalio

from lcd import LCD
from i2c_pcf8574_interface import I2CPCF8574Interface

# I2C display assignments
lcd_i2c = busio.I2C(board.GP1, board.GP0)
pcf_interface = I2CPCF8574Interface(lcd_i2c, 0x27)
DISPLAY = LCD(pcf_interface, num_rows=2, num_cols=16)

# Initialize rotary encoder and buttons
iopins = (board.GP2, board.GP3,board.GP4, board.GP5, board.GP6)
ENCODER = rotaryio.IncrementalEncoder(iopins[0], iopins[1])
ENC, RED, BLUE = (digitalio.DigitalInOut(pin) for pin in iopins[2:5])
for button in [ENC, RED, BLUE]:
    button.switch_to_input(digitalio.Pull.UP)
