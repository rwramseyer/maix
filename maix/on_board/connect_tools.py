# connect_tools.py
# Tools for Maixduino ESP32 connection

import network
from fpioa_manager import fm


def esp32_init(force=False):
    """
    Initialize Maixduino ESP32 with IO and SPI assignments
    :return: esp32 network object or NONE if a device already exists
    """
    esp32 = None
    exists = False

    # check if the ESP32 device was already initialized
    if not force:
        for key, val in locals().items():
            if isinstance(val, network.ESP32_SPI):
                exists = True
                print("An ESP32 device was already setup under name: ", key)
                esp32 = val

    # if not initialized or we want to re-initialize
    if not exists:
        # IO map for ESP32 on Maixduino
        fm.register(25, fm.fpioa.GPIOHS10)  # cs
        fm.register(8, fm.fpioa.GPIOHS11)  # rst
        fm.register(9, fm.fpioa.GPIOHS12)  # rdy
        fm.register(28, fm.fpioa.GPIOHS13)  # mosi
        fm.register(26, fm.fpioa.GPIOHS14)  # miso
        fm.register(27, fm.fpioa.GPIOHS15)  # sclk

        esp32 = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,
                                  rst=fm.fpioa.GPIOHS11,
                                  rdy=fm.fpioa.GPIOHS12,
                                  mosi=fm.fpioa.GPIOHS13,
                                  miso=fm.fpioa.GPIOHS14,
                                  sclk=fm.fpioa.GPIOHS15)

    return esp32


def do_connection(esp, ssid, password, tries=3):
    """
    Connect device to WiFi
    :param esp: esp32 network object
    :param ssid: ssid of WiFi AP to connect to
    :param password: password of WiFi AP to connect to
    :return: None
    """
    if not esp.isconnected():
        print("connecting WiFi now...")

        errors = 0
        while errors < tries and not esp.isconnected():
            try:
                esp.connect(ssid, password)
            except Exception as e:
                errors += 1
                print("connection failed, trying again")

        if esp.isconnected():
            print("successfully connected to " + ssid)
            esp.ifconfig()
        else:
            print("failed to connect after " + str(tries) + " tries")

    else:
        print("already connected")
