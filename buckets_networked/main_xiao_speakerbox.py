import espnow  # type: ignore
from asyncio import sleep, run
from hardware import AUDIO_OUT
from audio_commands import Sound_Control

e = espnow.ESPNow()

sounds = Sound_Control(AUDIO_OUT)
sounds.set_vol(30)


async def countdown():
    for i in range(10, -1, -1):
        sounds.play_track(i + 15)
        await sleep(1)


async def main():
    message = b"empty"
    msg_dec = message.decode()
    while True:
        try:
            msg = e.read()
            if msg.msg is not None and msg.msg != message:
                message = msg.msg
                msg_dec = message.decode()
                if msg_dec == "Start":
                    sounds.play_track(28)
                elif msg_dec == "60":
                    sounds.play_track(27)
                elif msg_dec == "30":
                    sounds.play_track(26)
                elif msg_dec == "10":
                    await countdown()
                elif msg_dec in ["Pause", "Resume"]:
                    sounds.play_track(35)
        except Exception:
            pass


if __name__ == "__main__":
    run(main())
