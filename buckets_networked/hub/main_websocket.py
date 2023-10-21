from time import monotonic
import json
import board
import neopixel
import socketpool
import wifi
import os
from adafruit_httpserver import Server, Request, Response, Websocket, GET, POST

pixel_pin = board.NEOPIXEL  # Change to the appropriate pin for your board
num_pixels = 1  # Change to the number of NeoPixels on your strip
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2)

font_family = "monospace"

ssid = os.getenv("AP_SSID")
password = os.getenv("AP_PASSWORD")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

wifi.radio.start_ap(ssid, password)
print("Connected to", ssid)

websocket: Websocket = None


@server.route("/", GET)
def client(request: Request):
    return Response(request, "index_websocket.html", "text/html")


@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket  # pylint: disable=global-statement
    if websocket is not None:
        websocket.close()  # Close any existing connection
    websocket = Websocket(request)
    return websocket


server.start(host=str(os.getenv("AP_IP")), port=80)
next_message_time = monotonic()
team_message_time = monotonic()
timer = 300
dataDict = {"timer": timer, "bucket1": "Red"}
while True:
    server.poll()

    if websocket is not None:
        if (data := websocket.receive(True)) is not None:
            r, g, b = int(data[1:3], 16), int(data[3:5], 16), int(data[5:7], 16)
            pixels.fill((r, g, b))

    if websocket is not None and monotonic() > next_message_time + 1:
        timer -= 1
        timestr = f"{timer // 60:02}:{timer % 60:02}"
        dataDict["timer"] = timestr
        json_string = json.dumps(dataDict)
        websocket.send_message(json_string)
        next_message_time = monotonic()

    if monotonic() > team_message_time + 2.5:
        dataDict["bucket1"] = "Blue" if dataDict["bucket1"] == "Red" else "Red"
        team_message_time = monotonic()
