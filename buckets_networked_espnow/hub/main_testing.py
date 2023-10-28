import espnow  # type: ignore
from time import monotonic
from hardware import DISPLAY, AUDIO_OUT
from audio_commands import Sound_Control

e = espnow.ESPNow()
peer = espnow.Peer(mac=b"\xf4\x12\xfa\xce\xd8\x28")
e.peers.append(peer)
packets = []

sounds = Sound_Control(AUDIO_OUT)

timer_time = monotonic()
read_time = monotonic()
timer = -1
message = b"wait"
msg_dec = message.decode()
while True:
    if monotonic() - timer_time >= 1:
        timer += 1
        timer_time = monotonic()
        e.send(str(timer))
        DISPLAY.clear()
        DISPLAY.write(
            f"Timer: {timer // 60:02d}:{timer % 60:02d}\nNode team: {msg_dec}"
        )
    if monotonic() - read_time >= 0.1:
        read_time = monotonic()
        try:
            packet = e.read()
            if packet.msg is not None:
                if packet.msg != message:
                    message = packet.msg
                    msg_dec = message.decode()
                    DISPLAY.clear()
                    DISPLAY.write(
                        f"Timer: {timer // 60:02d}:{timer % 60:02d}\nNode team: {msg_dec}"
                    )
                    if msg_dec == "Red":
                        sounds.play_track(11)
                    elif msg_dec == "Blue":
                        sounds.play_track(12)
        except Exception:
            pass
