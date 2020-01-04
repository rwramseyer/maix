import network
import wifi  # "wifi.py" holds the WIFI_SSID and WIFI_PASSWD values

WIFI_SSID = wifi.WIFI_SSID
WIFI_PASSWD = wifi.WIFI_PASSWD

# IO map for ESP32 on Maixduino
fm.register(25, fm.fpioa.GPIOHS10)  # cs
fm.register(8, fm.fpioa.GPIOHS11)  # rst
fm.register(9, fm.fpioa.GPIOHS12)  # rdy
fm.register(28, fm.fpioa.GPIOHS13)  # mosi
fm.register(26, fm.fpioa.GPIOHS14)  # miso
fm.register(27, fm.fpioa.GPIOHS15)  # sclk

nic = network.ESP32_SPI(cs=fm.fpioa.GPIOHS10,
                        rst=fm.fpioa.GPIOHS11,
                        rdy=fm.fpioa.GPIOHS12,
                        mosi=fm.fpioa.GPIOHS13,
                        miso=fm.fpioa.GPIOHS14,
                        sclk=fm.fpioa.GPIOHS15)

if not nic.isconnected():
    print("connecting WiFi now...")
    try:
        err = 0
        while 1:
            try:
                nic.connect(WIFI_SSID, WIFI_PASSWD)
            except Exception:
                err += 1
                print("Connection failed, trying again")
                if err > 3:
                    raise Exception("Connect AP fail")
                continue
            break
        nic.ifconfig()
    except Exception:
        pass
    finally:
        if nic.isconnected():
            print("successfully connected to " + WIFI_SSID)
else:
    print("already connected")
