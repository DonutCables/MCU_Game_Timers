# type: ignore
"""
Hardware declarations for the timer project.
Used to easily change pin connections without changing the primary code.
This file is for the Speakerbox components.
"""
import board
from busio import UART

# UART audio output
try:
    AUDIO_OUT = UART(board.IO43, board.IO44, baudrate=9600)
except Exception as e:
    print("AUDIO_OUT failed")
    print(e)
    pass
