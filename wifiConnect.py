import network
from temp_data import Network


def do_connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
        ip = sta_if.ifconfig()[0]
        return ip


def get_ip():
    if network.WLAN().isconnected():
        return network.ifconfig()[0]
    else:
        return "0.0.0.0"


def scan_networks():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    nets = sta_if.scan()
    networks = []
    # Convert dict to list of objects
    i = 0
    for n in nets:
        networks.append(Network(i, n[0].decode("utf-8"), n[3], '', n[5],))
        # Sort
        networks.sort(key=lambda n: (str(n.connected), n.ssid), reverse=True)
    return networks


def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='EMON')
    ap.config(authmode=3, password='whatnick')
    return ap
