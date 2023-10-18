import board
import neopixel
import socketpool
import wifi
import os
import time
from adafruit_httpserver import Server, Request, Response, POST

# Set up the NeoPixel strip
pixel_pin = board.NEOPIXEL  # Change to the appropriate pin for your board
num_pixels = 1  # Change to the number of NeoPixels on your strip
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2)

font_family = "monospace"
temp_test = 69
unit = "F"

# Connect to Wi-Fi access point
ssid = os.getenv("AP_SSID")
password = os.getenv("AP_PASSWORD")

wifi.radio.start_ap(ssid, password)
print("Connected to", ssid)

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

# Create an HTTP server
server = Server(pool, "/static", debug=True)


# Define a request handler for setting the NeoPixel color
def webpage():
    html = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    html{{font-family: {font_family}; background-color: lightgrey;
    display:inline-block; margin: 0px auto; text-align: center;}}
      h1{{color: deeppink; width: 200; word-wrap: break-word; padding: 2vh; font-size: 35px;}}
      p{{font-size: 1.5rem; width: 200; word-wrap: break-word;}}
      .button{{font-family: {font_family};display: inline-block;
      background-color: black; border: none;
      border-radius: 4px; color: white; padding: 16px 40px;
      text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}}
      p.dotted {{margin: auto;
      width: 75%; font-size: 25px; text-align: center;}}
    </style>
    </head>
    <body>
    <title>Pico W HTTP Server</title>
    <h1>Pico W HTTP Server</h1>
    <br>
    <p class="dotted">This is a Pico W running an HTTP server with CircuitPython.</p>
    <br>
    <p class="dotted">The current ambient temperature near the Pico W is
    <span style="color: deeppink;">{temp_test:.2f}°{unit}</span></p><br>
    <h1>Control the LED on the Pico W with these buttons:</h1><br>
    <form accept-charset="utf-8" method="POST">
    <button class="button" name="LED ON" value="ON" type="submit">LED ON</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="LED OFF" value="OFF" type="submit">LED OFF</button></a></p></form>
    <h1>Party?</h>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="party" value="party" type="submit">PARTY!</button></a></p></form>
    </body></html>"""
    return html


#  route default static IP
@server.route("/")
def base(request: Request):  # pylint: disable=unused-argument
    #  serve the HTML f string
    #  with content type text/html
    return Response(request, f"{webpage()}", content_type="text/html")


#  if a button is pressed on the site
@server.route("/", POST)
def buttonpress(request: Request):
    #  get the raw text
    raw_text = request.raw_request.decode("utf8")
    print(raw_text)
    #  if the led on button was pressed
    if "ON" in raw_text:
        #  turn on the onboard LED
        pixels.fill((255, 0, 0))
    #  if the led off button was pressed
    if "OFF" in raw_text:
        #  turn the onboard LED off
        pixels.fill((0, 255, 0))
    #  if the party button was pressed
    if "party" in raw_text:
        #  toggle the parrot_pin value
        pixels.fill((0, 0, 255))
    #  reload site
    return Response(request, f"{webpage()}", content_type="text/html")


server.start(host=str(os.getenv("AP_IP")), port=80)

delay = time.monotonic()
while True:
    if time.monotonic() - delay > 1:
        temp_test += 1
        delay = time.monotonic()
    server.poll()
