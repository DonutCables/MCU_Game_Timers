import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("waffle","mnementh13")
print(wlan.isconnected())