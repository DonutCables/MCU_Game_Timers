import traceback
import time
import gc
from adafruit_ble import BLERadio
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement



time.sleep(3)  #### wait for serial


ble = BLERadio()
while True:
    print("scanning")
    # found = set()
    # scan_responses = set()
    # By providing Advertisement as well we include everything, not just specific advertisements.
    try:
        found = set()
        for advertisement in ble.start_scan(ProvideServicesAdvertisement, Advertisement, extended=True, buffer_size=1024):
            addr = advertisement.address
            # if advertisement.scan_response and addr not in scan_responses:
            #     scan_responses.add(addr)
            # el
            if not advertisement.scan_response and addr not in found:
                found.add(addr)
            else:
                continue
            try:
                print(addr, advertisement.complete_name)  # UnicodeError:  # IndexError: index out of range  # TypeError: object with buffer protocol required
                # print("\t" + repr(advertisement), advertisement.short_name, advertisement.complete_name, advertisement.appearance, advertisement.rssi)  # OverflowError: value must fit in 1 byte(s)
            except (UnicodeError, OverflowError, IndexError, TypeError) as ex:
                traceback.print_exception(ex, ex, ex.__traceback__)
                continue
            if advertisement.complete_name == "timer_bucket":
                try:
                    connection = ble.connect(addr)
                    print("connected to", addr)
                    connection.disconnect()
                    print("disconnected from", addr)
                except Exception as ex:
                    traceback.print_exception(ex, ex, ex.__traceback__)           
    except (MemoryError, RuntimeError) as ex:  # RuntimeError: buffer too small  # RuntimeError: buffer size must match format
        print("scan stopping...")
        ble.stop_scan()
        traceback.print_exception(ex, ex, ex.__traceback__)
        print(f"{gc.mem_free()=}")
        gc.collect()
        print(f"{gc.mem_free()=}")
        # continue

    print("scan done")
    time.sleep(15)