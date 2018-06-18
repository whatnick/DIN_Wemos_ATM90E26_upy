import network

def do_connect(ssid,password):
    import network
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
