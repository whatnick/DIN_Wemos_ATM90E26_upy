from machine import I2C,Pin,SPI
from ssd1306 import SSD1306_I2C
import socket
from atm90e26_SPI import *

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('linuxconfau', 'sydney2018')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000)
lcd = SSD1306_I2C(64,48,i2c)
lcd.text("Whatnick",0,0)
lcd.text("Energy",0,16)
lcd.text("Monitor",0,32)
lcd.show()

sck = machine.Pin(14,machine.Pin.OUT)
mosi = machine.Pin(13,machine.Pin.OUT)
miso = machine.Pin(12,machine.Pin.IN)
cs1 = machine.Pin(0,machine.Pin.OUT)
cs2 = machine.Pin(15,machine.Pin.OUT)

do_connect()
time.sleep(2)

spi = machine.SPI(baudrate=200000,bits=8,polarity=1,phase=1,firstbit=machine.SPI.MSB,sck=sck,mosi=mosi,miso=miso)

all_ics = [ATM90E26_SPI(spi,cs1),ATM90E26_SPI(spi,cs2)]

while True:
	ic_id = 0
	for energy_ic in all_ics:
		print("Meter ID:",ic_id)
		sys_val = energy_ic.GetSysStatus()
		print("Sys Status:",hex(sys_val))
		met_val = energy_ic.GetMeterStatus()
		print("Met Status:",hex(met_val))
		voltage = energy_ic.GetLineVoltage()
		print("Voltage:",voltage)
		current = energy_ic.GetLineCurrent()
		print("Current:",current)
		power = energy_ic.GetActivePower()
		print("Power:",power)
		
		lcd.fill(0)
		lcd.text("Meter:"+str(ic_id),0,0)
		lcd.text("V:"+str(voltage),0,12)
		lcd.text("I:"+str(current),0,24)
		lcd.show()

		url = 'https://emoncms.org/input/post?json={power'+str(ic_id)+':'+str(power)+'}&apikey=API_KEY'
		http_get(url)
		ic_id += 1
		time.sleep(1)
	lcd.fill(0)
	lcd.show()	
	time.sleep(10)
