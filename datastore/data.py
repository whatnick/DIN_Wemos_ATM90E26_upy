# Create data sources and populate with sample data
import ujson

# TODO: Make decorator?

def make_dbs():
    # Create new databases if they don't exist
    network_db()
    logger_db()
    config_db()

def network_db():
    try:
        f = open("datastore/network.json", "r")
    except OSError:
        f = open("datastore/network.json", "w")
        db = {}
        db[b"network1"] = b"didit"
        db[b"network2"] = b""
        db[b"network3"] = b""
        db[b"HiddenNetwork"] = b"shhhh!"
        ujson.dump(db,f)
        f.flush()
        f.close()

def logger_db():
    try:
        f = open("datastore/logger.json", "r")
    except OSError:
        f = open("datastore/logger.json", "w")
        db = {}
        db[b"service"] = "awsiot"
        db[b"awsiot"] = ujson.dumps({
            "name": "Amazon Web Service, IoT",
            "cert": 12345678,
            "key": "123456g789p",
            "subdomain": "Saturn",
            "region": "Milkyway",
        })
        db[b"thingspeak"] = ujson.dumps({
            "name": "ThingSpeak",
            "key": "123456g789p"
        })
        ujson.dump(db,f)
        f.flush()
        f.close()

def config_db():
    try:
        f = open("datastore/config.json", "r")
    except OSError:
        f = open("datastore/config.json", "w")
        db = {}
        db[b"eci1_crc1"] = b"0"
        db[b"eci1_crc2"] = b"0"
        db[b"eci1_gain"] = b"0"
        db[b"eci1_ugain"] = b"0"
        db[b"eci2_crc1"] = b"0"
        db[b"eci2_crc2"] = b"0"
        db[b"eci2_gain"] = b"0"
        db[b"eci2_ugain"] = b"0"
        ujson.dump(db,f)
        f.flush()
        f.close()    