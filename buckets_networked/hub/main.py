import board
import busio
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_wifimanager as wifimanager
import adafruit_esp32spi.adafruit_esp32spi as adafruit_esp32spi
import wifi_info

esp32_cs = DigitalInOut(board.D22)
esp32_ready = DigitalInOut(board.D17)
esp32_reset = DigitalInOut(board.D27)

lock_count = 0

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
if not spi.try_lock():
    if lock_count < 10:
        try:
            spi.configure(baudrate=921600)
        except:
            print("lock failed")
            lock_count += 1
            pass


esp = adafruit_esp32spi.ESP_SPIcontrol(
    spi, esp32_cs, esp32_ready, esp32_reset, debug=True
)

# Configure the access point (AP) settings
ap_ssid = "MyAP"  # Change this to your desired SSID
ap_password = "MyPassword"  # Change this to your desired password

ap = wifimanager.ESPSPI_WiFiManager(esp, wifi_info.secrets)
ap.create_ap()

print("Access Point started with SSID:", ap_ssid)

while True:
    pass  # Your code logic here for handling client connections, etc.
