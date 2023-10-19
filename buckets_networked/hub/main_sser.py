from time import monotonic
import board
import neopixel
import socketpool
import wifi
import os
from adafruit_httpserver import Server, Request, Response, SSEResponse, GET, POST

pixel_pin = board.NEOPIXEL  # Change to the appropriate pin for your board
num_pixels = 1  # Change to the number of NeoPixels on your strip
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2)

font_family = "monospace"
temp_test = 69
unit = "F"

ssid = os.getenv("AP_SSID")
password = os.getenv("AP_PASSWORD")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

wifi.radio.start_ap(ssid, password)
print("Connected to", ssid)

sse_response: SSEResponse = None
next_event_time = monotonic()


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
    <title>Timer Buckets</title>
    <h1>ESP32S3 Timer Bucket Server</h1>
    <br>
    <p class="dotted">Example page hosting timer bucket information.</p>
    <br>
    <p class="dotted">The current timer value is <strong>-</strong></p>
    <script>
    const eventSource = new EventSource("/connect-client");
    const timer = document.querySelector("strong");
    eventSource.onmessage = (event) => timer.textContent = event.data;
    eventSource.onerror = (error) => timer.textContent = error;
    </script>
    <span style="color: deeppink;">
    </span><br>
    <h1>Control the LED on the Pico W with these buttons:</h1><br>
    <form accept-charset="utf-8" method="POST">
    <button class="button" name="LED RED" value="RED" type="submit">LED RED</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="LED GREEN" value="GREEN" type="submit">LED GREEN</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="LED BLUE" value="BLUE" type="submit">LED BLUE</button></a></p></form>
    </body></html>"""
    return html


@server.route("/", GET)
def client(request: Request):
    return Response(request, webpage(), content_type="text/html")


@server.route("/", POST)
def buttonpress(request: Request):
    #  get the raw text
    raw_text = request.raw_request.decode("utf8")
    print(raw_text)
    if "RED" in raw_text:
        pixels.fill((255, 0, 0))
    if "GREEN" in raw_text:
        pixels.fill((0, 255, 0))
    if "BLUE" in raw_text:
        pixels.fill((0, 0, 255))
    #  reload site
    return Response(request, webpage(), content_type="text/html")


@server.route("/connect-client", GET)
def connect_client(request: Request):
    global sse_response  # pylint: disable=global-statement
    if sse_response is not None:
        sse_response.close()  # Close any existing connection
    sse_response = SSEResponse(request)
    return sse_response


server.start(host=str(os.getenv("AP_IP")), port=80)
timer = 300

while True:
    server.poll()
    # Send an event every second
    if sse_response is not None and next_event_time < monotonic():
        timer -= 1
        timestr = f"{timer // 60:02}:{timer % 60:02}"
        sse_response.send_event(str(timestr))
        next_event_time = monotonic() + 1
