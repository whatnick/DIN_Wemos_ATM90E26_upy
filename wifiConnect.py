import network
import machine
import ubinascii
import btree


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
    # Note: Networks may appear multiple times. raw list is reduced to single instance of each network
    networks = {}
    for n in nets:
        ssid = n[0].decode("utf-8")
        if ssid not in networks:
            networks[ssid] = {
                "ssid": ssid,
                "str":n[3],
                "pwd":''
            }
        elif n[3] > networks[ssid]['str']:
            networks[n[0].decode("utf-8")]['str'] = n[3]
    # Incorporate saved passwords
    f = open("datastore/network.db", "r+b")
    db = btree.open(f)
    for key in db:
        if key.decode("utf-8") in networks:
            networks[key.decode("utf-8")]['pwd'] = db[key].decode("utf-8")
    db.close()
    f.close()
    networks = list(networks.values())
    # TODO: include 'connected' in sort order)
    networks.sort(key=lambda n:(n['pwd'], n['str']), reverse=True)
    return networks


def start_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='EMON_'+str(ubinascii.hexlify(machine.unique_id()))[-4:])
    ap.config(authmode=3, password='whatnick')
    return ap
