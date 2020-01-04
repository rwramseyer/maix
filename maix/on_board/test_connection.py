import network
import net_info  # "net_info.py" holds the WIFI_SSID and WIFI_PASSWD values

WIFI_SSID = net_info.WIFI_SSID
WIFI_PASSWD = net_info.WIFI_PASSWD


def esp32_init():
    """
    Initialize Maixduino ESP32 with IO and SPI assignments
    :return: network object
    """
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


# check if already connected
if 'nic' not in locals():
    nic = esp32_init()

do_connection(nic, WIFI_SSID, WIFI_PASSWD)
