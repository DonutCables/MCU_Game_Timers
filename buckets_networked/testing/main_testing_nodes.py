from time import monotonic
from hardware import REDB, BLUEB, RED_LED, BLUE_LED, DISPLAY
import espnow  # type: ignore

e = espnow.ESPNow()
peer = espnow.Peer(mac=b"")
e.peers.append(peer)

read_time = monotonic()
timer = -1
team = "Green"
e.send(str(team))
DISPLAY.write(f"Team: {team}\nHub time: {timer // 60:02d}:{timer % 60:02d}")
while True:
    REDB.update()
    BLUEB.update()
    if REDB.pressed:
        team = "Red"
        RED_LED.value = True
        BLUE_LED.value = False
        e.send(str(team))
        DISPLAY.clear()
        DISPLAY.write(f"Team: {team}\nHub time: {timer // 60:02d}:{timer % 60:02d}")
    if BLUEB.pressed:
        team = "Blue"
        RED_LED.value = False
        BLUE_LED.value = True
        e.send(str(team))
        DISPLAY.clear()
        DISPLAY.write(f"Team: {team}\nHub time: {timer // 60:02d}:{timer % 60:02d}")
    if monotonic() - read_time >= 0.1:
        read_time = monotonic()
        try:
            packet = e.read()
            if packet.msg is not None:
                timer = int(packet.msg)
                if timer == 0:
                    team = "Green"
                    RED_LED.value = False
                    BLUE_LED.value = False
                DISPLAY.clear()
                DISPLAY.write(
                    f"Team: {team}\nHub time: {timer // 60:02d}:{timer % 60:02d}"
                )
        except:
            pass
