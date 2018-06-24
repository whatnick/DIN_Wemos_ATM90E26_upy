from machine import I2C, Pin, SPI
from ssd1306 import SSD1306_I2C
import socket
from atm90e26_SPI import *
from wifiConnect import do_connect
import ntptime

CARBON_PORT = 2003
CARBON_SERVER = '192.168.43.107'


def graphite_send(var, val):
    import socket
    message = 'whatnick.emon.%s %f %d\n' % (var, val, int(time.time()))
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message)
    sock.close()

'''
ESP8266	ESP32	ESP8266	ESP32
TX		TXD		RST		RST
RX		RXD		A0		SVP
IO5		IO22	IO16	IO26
IO4		IO21	IO14	IO18
IO0		IO17	IO12	IO19
IO2		IO16	IO13	IO23
GND		GND		IO15	IO5
5V		VCC		3V3		3.3V
'''

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = SSD1306_I2C(64, 48, i2c)
lcd.text("Whatnick", 0, 0)
lcd.text("Energy", 0, 16)
lcd.text("Monitor", 0, 32)
lcd.show()

sck = machine.Pin(18, machine.Pin.OUT)
mosi = machine.Pin(23, machine.Pin.OUT)
miso = machine.Pin(19, machine.Pin.IN)
#Chip select pins
cs1 = machine.Pin(5, machine.Pin.OUT)
cs2 = machine.Pin(17, machine.Pin.OUT)

do_connect('blynkspot', 'blynkpass')
time.sleep(2)
ntptime.settime()

spi = machine.SPI(baudrate=200000, bits=8, polarity=1, phase=1,
                  firstbit=machine.SPI.MSB, sck=sck, mosi=mosi, miso=miso)

all_ics = [ATM90E26_SPI(spi, cs1), ATM90E26_SPI(spi, cs2)]

while True:
    ic_id = 0
    for energy_ic in all_ics:
        print("Meter ID:", ic_id)
        sys_val = energy_ic.GetSysStatus()
        print("Sys Status:", hex(sys_val))
        met_val = energy_ic.GetMeterStatus()
        print("Met Status:", hex(met_val))
        voltage = energy_ic.GetLineVoltage()
        print("Voltage:", voltage)
        current = energy_ic.GetLineCurrent()
        print("Current:", current)
        power = energy_ic.GetActivePower()
        print("Power:", power)

        lcd.fill(0)
        lcd.text("Meter:"+str(ic_id), 0, 0)
        lcd.text("V:"+str(voltage), 0, 12)
        lcd.text("I:"+str(current), 0, 24)
        lcd.show()

        graphite_send("pow"+str(ic_id), power)

        ic_id += 1
        time.sleep(1)
    lcd.fill(0)
    lcd.show()
    time.sleep(10)
