# type: ignore
"""
Hardware declarations for the timer project.
Used to easily change pin connections without changing the primary code.
"""
import board
from busio import UART

# UART audio output
try:
    AUDIO_OUT = UART(board.IO43, board.IO44, baudrate=9600)
except Exception:
    print("AUDIO_OUT failed")
    pass
