import espnow  # type: ignore
from time import monotonic, sleep
from hardware import AUDIO_OUT
from audio_commands import Sound_Control

e = espnow.ESPNow()

sounds = Sound_Control(AUDIO_OUT)
sounds.set_vol(30)


def countdown():
    for i in range(10, -1, -1):
        sounds.play_track(i + 15)
        sleep(1)


read_time = monotonic()
message = b"empty"
msg_dec = message.decode()
while True:
    if monotonic() - read_time >= 0.1:
        read_time = monotonic()
        msg = e.read()
        try:
            if msg.msg is not None and msg.msg != message:
                message = msg.msg
                msg_dec = message.decode()
                if msg_dec == "Start":
                    sounds.play_track(28)
                elif msg_dec == "Red":
                    sounds.play_track(11)
                elif msg_dec == "Blue":
                    sounds.play_track(12)
                elif msg_dec == "60":
                    sounds.play_track(27)
                elif msg_dec == "30":
                    sounds.play_track(26)
                elif msg_dec == "10":
                    countdown()
                elif msg_dec == "End":
                    sounds.play_track(2)
                elif msg_dec in ["Pause", "Resume"]:
                    sounds.play_track(35)
        except Exception:
            pass
