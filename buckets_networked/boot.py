import board
import supervisor
import digitalio

button = digitalio.DigitalInOut(board.IO7)
button.switch_to_input(pull=digitalio.Pull.UP)

if not button.value:
    supervisor.runtime.autoreload = False
elif button.value:
    supervisor.runtime.autoreload = True
