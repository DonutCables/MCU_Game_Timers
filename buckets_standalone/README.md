# Standalone codebase
Here is where the code for the standalone versions of the buckets lives. This version has all game modes that don't require external control and requires no networking.

This version is built targetting a Pi Pico, and as such the `hardware.py` file has premade pin mappings for it. If you want to run this on a different board, you will need to change the pin mappings in that file. This version is also using CircuitPython 8 and may or may not be updated to newer versions.