# Standalone codebase
Here is where the code for the standalone versions of the buckets lives. This version has all game modes that don't require external control, and requires no networking.

*main.py* works with both MicroPython and CircuitPython, but requires the specific *lib* folder for either. The MicroPython version may be deprecated in the future when the Pico W gains ble access in CircuitPython.