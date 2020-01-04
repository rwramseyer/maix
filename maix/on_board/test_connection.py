from net_info import get_wifi_info # "net_info.py" holds the WIFI_SSID and WIFI_PASSWD values
from connect_tools import esp32_init, do_connection

# setup wifi information
WIFI_SSID, WIFI_PASSWD = get_wifi_info()

# initialize nic
nic = esp32_init()

# if nic initialized, then connect
if nic:
    do_connection(nic, WIFI_SSID, WIFI_PASSWD)
