import network
from temp_data import Network

def do_connect(ssid,password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid,password)
        while not sta_if.isconnected():
            pass
	ip = sta_if.ifconfig()[0]
	return ip

def get_ip():
	sta_if = network.WLAN(network.STA_IF)
	if(sta_if.isconnected()):
		return sta_if.ifconfig()[0]

def scan_networks():
	wlan = network.WLAN(network.STA_IF)
	nets = wlan.scan()
	networks = []
	# Convert dict to list of objects
	i = 0
	for n in nets:
		networks.append(Network(i,n[0].decode("utf-8") ,n[3],'',n[5],))
		# Sort
		networks.sort(key=lambda n:(str(n.connected), n.ssid), reverse=True)        
	return networks
