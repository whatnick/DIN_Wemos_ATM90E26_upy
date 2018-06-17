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

def networks():
    data = [
        {
            "id":0,
            "ssid":"Fon WiFi",
            "strength":-84,
            "pwd":'',
            "connected": False
        },{
            "id":1,
            "ssid":"Telstra5C49",
            "strength":-90,
            "pwd":'',
            "connected": False
        },{
            "id":2,
            "ssid":"TGP fastAir",
            "strength":-40,
            "pwd":"nevaguess;P",
            "connected": True
        },{
            "id":3,
            "ssid":"Telstra Air",
            "strength":-78,
            "pwd":"high-5ecurity",
            "connected": False
        },{
            "id":4,
            "ssid":"Telstra2EC8",
            "strength":-20,
            "pwd":'',
            "connected": False
        },{
            "id":5,
            "ssid":"Hal-North",
            "strength":-79,
            "pwd":'',
            "connected": False
        },{
            "id":6,
            "ssid":"myHiddenNetwork",
            "strength":0,
            "pwd":"sshhhhhhh!",
            "connected": False
        }
    ]
    networks = []
    # Convert dict to list of objects
    for n in data:
        networks.append(Network(n['id'],n['ssid'],n['strength'],n['pwd'],n['connected'],))
        # Sort
        networks.sort(key=lambda n:(str(n.connected), n.pwd, n.ssid), reverse=True)
        
    return networks


####################################
# Alerts
class Alert:
    def __init__(self,type='info',message=''):
        self.type = type
        self.message = message