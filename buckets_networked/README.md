# Networked codebase
Here is where the code for the networked versions of the buckets lives. This version has all game modes with external control enabled, and requires devices capable of ESP-NOW communication.

This version is built targetting a Xiao ESP32S3, and as such the `hardware.py` file has premade pin mappings for it. If you want to run this on a different board, you will need to change the pin mappings in that file.