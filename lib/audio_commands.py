from hardware import AUDIO

cmd_base = bytearray([0x7E, 0xFF, 0x06, 0x00, 0x00, 0x00, 0x00, 0xEF])

def play_track(track):
    play_track = cmd_base
    play_track[3] = 0x03
    play_track[6] = track
    AUDIO.write(play_track)

def vol_up():
    vol_up = cmd_base
    vol_up[3] = 0x04
    AUDIO.write(vol_up)

def vol_down():
    vol_down = cmd_base
    vol_down[3] = 0x05
    AUDIO.write(vol_down)

def set_vol(level):
    set_vol = cmd_base
    set_vol[3] = 0x06
    set_vol[6] = level
    AUDIO.write(set_vol)

def play_at_vol(track=01, vol=15):
    play_at_vol = cmd_base
    play_at_vol[3] = 0x22
    play_at_vol[5] = vol
    play_at_vol[6] = track
    AUDIO.write(play_at_vol)
