import logging
import utemplate
import uasyncio
import picoweb
import ujson
import btree
import gc

# Uncomment to create new databases
from datastore import data
data.make_dbs()

from wifiConnect import *

first_run = True
if first_run:
    start_ap()
else:
    do_connect('blynkspot', 'blynkpass')
ip = get_ip()   

#ip = "127.0.0.1"

app = picoweb.WebApp(None)

# TODO: Refile classes (or remove them entirely, they may contribute to memory issues?)
class Alert:
    def __init__(self,type='info',message=''):
        self.type = type
        self.message = message
        
        
@app.route("/")
def index(req, resp):
    gc.collect()
    f = open("datastore/logger.json", "r")
    db = ujson.load(f)
    logger = db['service']
    f.close() 
    # TODO: Load dynamic content from datastore
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "index.html", ("[connected ssid here]", logger, "[version no. here]"))

@app.route("/networks", methods=['GET', 'POST'])
def networks(req, resp):
    gc.collect()
    if req.method == 'POST':
        f = open("datastore/network.json", "r")
        db = btree.open(f)
        yield from req.read_form_data()
        if req.form.get('connect'):
            # Save process form submission
            db[req.form.get('ssid')[0]] = req.form.get('pwd')[0].encode('utf-8')
            # TODO: attempt to connect to network requested in form
        elif req.form.get('forget'):
            del db[req.form.get('ssid')[0]]
        db.close()
        f.close()

    # TODO: discover which network is connected (if any)
    connected_network = 'network1'
    networks = scan_networks()
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "networks.html", (networks, connected_network))

@app.route("/logging", methods=['GET','POST'])
def logging(req, resp):
    gc.collect()
    f = open("datastore/logger.json", "r")
    db = ujson.load(f)
    f.close()
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
        f = open("datastore/logger.json", "w")
        ujson.dump(db,f)
        f.close()
        # TODO: Redirect not working?, memory problem?
        # TODO: Change redirect URL to dynamic value.
        yield from resp.awrite("HTTP/1.0 308 Redirect\r\n")
        yield from resp.awrite("Location: http://192.168.4.1:8081/\r\n")
    else:   
        yield from picoweb.start_response(resp)
        yield from app.render_template(resp, "logging.html",(db['thingspeak'], db['awsiot'], db['service']))
        f.close() 

@app.route("/hardware")
def device(req, resp):
    gc.collect()
    if req.method == 'POST':
        yield from req.read_form_data()
        #TODO: field validation
        f = open("datastore/config.json", "r")
        db = ujson.load(f)
        f.close()
        db[b"eci1_crc1"] = req.form.get("eci1_crc1")[0]
        db[b"eci1_crc2"] = req.form.get("eci1_crc2")[0]
        db[b"eci1_gain"] = req.form.get("eci1_gain")[0]
        db[b"eci1_ugain"] = req.form.get("eci1_ugain")[0]
        db[b"eci2_crc1"] = req.form.get("eci2_crc1")[0]
        db[b"eci2_crc2"] = req.form.get("eci2_crc2")[0]
        db[b"eci2_gain"] = req.form.get("eci2_gain")[0]
        db[b"eci2_ugain"] = req.form.get("eci2_ugain")[0]
        f = open("datastore/config.json", "w")
        ujson.dump(db,f)
        f.flush()
        f.close()
        # TODO: Redirect not working?, memory problem?
        yield from resp.awrite("HTTP/1.0 308 Redirect \r\n")
        yield from resp.awrite("Location: http://192.168.4.1:8081/\r\n")
    else:
        f = open("datastore/config.json", "r")
        db = ujson.load(f)
        # TODO: Check if passing db saves any *real* memory - is this a weird way to pass variables to template?
        yield from picoweb.start_response(resp)
        yield from app.render_template(resp, "hardware.html",(db,))
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