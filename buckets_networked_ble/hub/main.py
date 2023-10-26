import board
import busio
import json
import socketpool
import wifi
import os
from time import monotonic, sleep
from adafruit_httpserver import Server, Request, Response, Websocket, GET


# region wifi webpage setup
ssid = os.getenv("AP_SSID")
password = os.getenv("AP_PASSWORD")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True)

wifi.radio.start_ap(ssid, password)
print("Connected to", ssid)

websocket: Websocket = None


@server.route("/", GET)
def client(request: Request):
    return Response(request, "index.html", "text/html")


@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    global websocket  # pylint: disable=global-statement
    if websocket is not None:
        websocket.close()  # Close any existing connection
    websocket = Websocket(request)
    return websocket


@server.route("/get-data", GET)
def get_data(request: Request):
    return Response(request, json.dumps(dataDict), content_type="application/json")


server.start(host=str(os.getenv("AP_IP")), port=80)
# endregion

# region ble setup

# endregion


next_message_time = monotonic()
team_message_time = monotonic()
timer = 300
dataDict = {"timer": timer, "bucket1": "Red"}
while True:
    server.poll()
    if websocket is not None and monotonic() > next_message_time + 1:
        timer -= 1
        timestr = f"{timer // 60:02}:{timer % 60:02}"
        dataDict["timer"] = timestr
        json_string = json.dumps(dataDict)
        next_message_time = monotonic()
    if monotonic() > team_message_time + 2.5:
        dataDict["bucket1"] = "Blue" if dataDict["bucket1"] == "Red" else "Red"
        team_message_time = monotonic()

    sleep(0.01)
