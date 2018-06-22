### Dummy data ###
# NB. uTemplates use dot notation for variable references
# so data is often converted to objects here.

####################################
# Logging services

class Log_ts:
    def __init__(self, key=''):
        self.name = "ThingSpeak"
        self.key = key
class Log_awsiot:
    def __init__(self, cert='', key='', subdomain='', region=''):
        self.name = "AWS IoT"
        self.cert = cert
        self.key = key
        self.subdomain = subdomain
        self.region = region

log_ts = Log_ts()
log_aws = Log_awsiot('myCert.pem','myKey.key','myIoT','ap-southeast-2')
active_logger = "AWS IoT"

####################################
# Device Configuration

version = "0.0.0.3"
latest = "0.0.1.1"

class Eci:
    def __init__(self, name):
        self.name = name
        self.crc1 = 0
        self.crc2 = 0
        self.gain = 0
        self.ugain = 0
        

config = [ Eci('ECI1'), Eci('ECI2')]

 
####################################
# Networks

class Network:
    def __init__(self, id, ssid, strength, pwd, connected):
        self.id = id
        self.str = strength
        self.ssid = ssid
        self.pwd = pwd
        self.connected = connected


####################################
# Alerts
class Alert:
    def __init__(self,type='info',message=''):
        self.type = type
        self.message = message
