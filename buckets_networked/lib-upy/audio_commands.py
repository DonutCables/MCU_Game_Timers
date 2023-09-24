"""
A translation for making nice clean functions from the UART mishmash being sent to the module.
"""
from hardware import AUDIO_OUT


class Sound_Control:
    """Sound control via UART AUDIO_OUT object via Catalex protocol"""

    def __init__(self):
        self.AUDIO_OUT = AUDIO_OUT

    cmd_base = bytearray([0x7E, 0xFF, 0x06, 0x00, 0x00, 0x00, 0x00, 0xEF])

    def play_track(self, track: int):
        """Plays a track based on the numerical name"""
        play_track = self.cmd_base
        play_track[3] = 0x03
        play_track[6] = int(hex(track))
        AUDIO_OUT.write(play_track)

    def vol_up(self):
        """Increments volume by one"""
        vol_up = self.cmd_base
        vol_up[3] = 0x04
        AUDIO_OUT.write(vol_up)

    def vol_down(self):
        """Decrements volume by one"""
        vol_down = self.cmd_base
        vol_down[3] = 0x05
        AUDIO_OUT.write(vol_down)

    def set_vol(self, level=30):
        """Sets volume level from 0-30"""
        set_vol = self.cmd_base
        set_vol[3] = 0x06
        set_vol[6] = int(hex(level))
        AUDIO_OUT.write(set_vol)

    def play_at_vol(self, track=1, vol=30):
        """Plays a track at a set volume"""
        play_at_vol = self.cmd_base
        play_at_vol[3] = 0x22
        play_at_vol[5] = int(hex(vol))
        play_at_vol[6] = int(hex(track))
        AUDIO_OUT.write(play_at_vol)
