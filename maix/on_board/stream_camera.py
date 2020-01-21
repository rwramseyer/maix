# stream_camera.py
# Modified version of "demo_esp32_send_pic.py" located at
# https://github.com/sipeed/MaixPy_scripts/blob/master/network/demo_esp32_send_pic.py

import network, socket, time, sensor, image, lcd
from net_info import get_wifi_info, get_server_info
from connect_tools import esp32_init, do_connection


# initialize nic and connect to wifi
WIFI_SSID, WIFI_PASSWD = get_wifi_info()
nic = esp32_init()
do_connection(nic, WIFI_SSID, WIFI_PASSWD)

# initialize server information
SERVER_IP, SERVER_PORT = get_server_info()
addr = (SERVER_IP, SERVER_PORT)

# initialize clock
clock = time.clock()

# initialize camera & screen
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
# sensor.skip_frames(time = 2000)

TRIES = 10  # set number of errors allowed before re-connection established
QUALITY = 20  # set image quality

# main program loop
while True:
    if nic.isconnected():
        # create socket
        s = socket.socket()
        try:
            print("Connecting socket...")
            s.connect(addr)
        except Exception as e:
            print("Error:", e)
            s.close()
        s.settimeout(5)

        count = 0
        errors = 0

        # send image over socket loop
        while True:
            clock.tick()
            if errors > TRIES:
                print("socket broken")
                break

            # capture image
            img = sensor.snapshot()
            lcd.display(img)
            img = img.compress(quality=QUALITY)
            img_bytes = img.to_bytes()

            # send over socket
            try:
                send_len = s.send(img_bytes)
                if send_len == 0:
                    print("failed")
                    raise Exception("send fail")
            except OSError as e:
                if e.args[0] == 32:
                    print("no connection")
                    errors += 1
                    continue
                elif e.args[0] == 128:
                    print("Connection closed")
                    break
                else:
                    print("Unknown error", e)
            except Exception as e:
                print("send fail:", e)
                # time.sleep()
                errors += 1
                continue
            count += 1

            print("send:", count)
            print("fps:", clock.fps())
        s.close()
        print("socket closed")
    else:
        # attempt reconnection
        print("WiFi not connected, attempting to reconnect...")
        do_connection(nic, WIFI_SSID, WIFI_PASSWD)
