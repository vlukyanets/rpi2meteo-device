#!/usr/bin/python2.7
# 2016 (C) Valentin Lukyanets


import sys
import uuid


DEVICE_ID_FILENAME = 'rpi2meteo.deviceid'


def main():
    device_id = uuid.uuid4().hex
    with open(DEVICE_ID_FILENAME, "w") as f:
        f.write(device_id)
    print "Device ID:", device_id


if __name__ == "__main__":
    main()
    sys.exit()
