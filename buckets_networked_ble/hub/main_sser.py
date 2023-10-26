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


@server.route("/", GET)
def client(request: Request):
    return Response(request, "index_sser.html", "text/html")


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
    return Response(request, "index_sser.html", content_type="text/html")


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
