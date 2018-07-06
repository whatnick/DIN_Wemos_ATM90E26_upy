import logging
import utemplate
import uasyncio
import picoweb
import ujson
import btree
import gc

# Uncomment to create new databases
#from datastore import data
#data.make_dbs()

from wifiConnect import *

first_run = True
if first_run:
    start_ap()
else:
    do_connect('blynkspot', 'blynkpass')

ip = get_ip()   
network_list = scan_networks()

app = picoweb.WebApp(None)

# TODO: Refile classes (or remove them entirely, they may contribute to memory issues?)
class Alert:
    def __init__(self,type='info',message=''):
        self.type = type
        self.message = message
        
        
class Network:
    def __init__(self, ssid, pwd=None):
        self.ssid = ssid
        self.pwd = pwd
    
    def __str__(self):
        return self.ssid 


@app.route("/")
def index(req, resp):
    gc.collect()
    # TODO: Load dynamic content from datastore
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "index.html", ("[connected ssid here]", "[logging service here]", "[version no. here]"))

@app.route("/networks", methods=['GET', 'POST'])
def networks(req, resp):
    gc.collect()
    f = open("datastore/network.db", "r+b")
    db = btree.open(f)
    if req.method == 'POST':
        yield from req.read_form_data()
        if req.form.get('connect'):
            # Save process form submission
            db[req.form.get('ssid')[0]] = req.form.get('pwd')[0].encode('utf-8')
            # TODO: attempt to connect to network requested in form
        elif req.form.get('forget'):
            del db[req.form.get('ssid')[0]]

    # Load networks from db
    # TODO: discover which network is connected (if any)
    connected_network = 'network1'
    # TODO: Load network data from WIFI and merge with saved data
    networks = []
    for key in db:
        networks.append(Network(key.decode("utf-8"), db[key].decode("utf-8")))
    db.close()
    f.close()
    # TODO: sort network list: 1)connected 2)remembered 3)discovered secondary sort by signal strength if possible
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "networks.html", (networks, connected_network))

@app.route("/logging", methods=['GET','POST'])
def logging(req, resp):
    gc.collect()
    f = open("datastore/logger.db", "r+b")
    db = btree.open(f)
    if req.method == 'POST':
        yield from req.read_form_data()
        db["service"] = req.form.get('service')[0]
        if req.form.get('service')[0] == "thingspeak":
            db[b"thingspeak"] = ujson.dumps({
                "name": "ThingSpeak",
                "key": req.form.get('ts_key')[0]
            })
        elif req.form.get('service')[0] == "awsiot":
            db[b"awsiot"] = ujson.dumps({
                "name": "Amazon Web Service, IoT",
                "cert": req.form.get('cert')[0],
                "key": req.form.get('aws_key')[0],
                "subdomain": req.form.get('subdomain')[0],
                "region": req.form.get('region')[0],
            })
        db.close()
        f.close()    
        # TODO: Crosscheck this is the correct way to do redirection after form processing
        yield from resp.awrite("HTTP/1.0 308 Redirect\r\n")
        yield from resp.awrite("Location:/ \r\n")
    else:   
        yield from picoweb.start_response(resp)
        yield from app.render_template(resp, "logging.html",(ujson.loads(db['thingspeak']), ujson.loads(db['awsiot']), db['service'].decode('utf-8')))
        db.close()
        f.close() 

@app.route("/hardware")
def device(req, resp):
    gc.collect()
    if req.method == 'POST':
        yield from req.read_form_data()
        #TODO: field validation
        f = open("datastore/config.db", "r+b")
        db = btree.open(f)
        db[b"eci1_crc1"] = req.form.get("eci1_crc1")[0]
        db[b"eci1_crc2"] = req.form.get("eci1_crc2")[0]
        db[b"eci1_gain"] = req.form.get("eci1_gain")[0]
        db[b"eci1_ugain"] = req.form.get("eci1_ugain")[0]
        db[b"eci2_crc1"] = req.form.get("eci2_crc1")[0]
        db[b"eci2_crc2"] = req.form.get("eci2_crc2")[0]
        db[b"eci2_gain"] = req.form.get("eci2_gain")[0]
        db[b"eci2_ugain"] = req.form.get("eci2_ugain")[0]
        db.close()
        f.close()
        # Redirect to homepage
        yield from resp.awrite("HTTP/1.0 308 Redirect\r\n")
        yield from resp.awrite("Location:/ \r\n")
    f = open("datastore/config.db", "r+b")
    db = btree.open(f)
    # TODO: Check if passing db saves any *real* memory.
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "hardware.html",(db,))
    db.close()
    f.close()

@app.route("/firmware")
def device(req, resp):
    gc.collect()
    # TODO: Implement dynamic data
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "firmware.html", ("0.0.1", "0.0.2"))

import logging
logging.basicConfig(level=logging.INFO)

app.run(debug=True, host=ip)