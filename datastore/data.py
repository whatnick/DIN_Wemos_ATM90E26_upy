# Create data sources and populate with sample data
import btree
import ujson

# TODO: Make decorator?

def make_dbs():
    # Create new databases if they don't exist
    network_db()
    logger_db()
    config_db()

def network_db():
    try:
        f = open("datastore/network.db", "r+b")
    except OSError:
        f = open("datastore/network.db", "w+b")
        db = btree.open(f)
        db[b"network1"] = b"didit"
        db[b"network2"] = b""
        db[b"network3"] = b""
        db[b"HiddenNetwork"] = b"shhhh!"
        db.close()
        f.close()

def logger_db():
    try:
        f = open("datastore/logger.db", "r+b")
    except OSError:
        f = open("datastore/logger.db", "w+b")
        db = btree.open(f)
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

        db.close()
        f.close()

def config_db():
    try:
        f = open("datastore/config.db", "r+b")
    except OSError:
        f = open("datastore/config.db", "w+b")
        db = btree.open(f)
        db[b"eci1_crc1"] = b"0"
        db[b"eci1_crc2"] = b"0"
        db[b"eci1_gain"] = b"0"
        db[b"eci1_ugain"] = b"0"
        db[b"eci2_crc1"] = b"0"
        db[b"eci2_crc2"] = b"0"
        db[b"eci2_gain"] = b"0"
        db[b"eci2_ugain"] = b"0"
        db.close()
        f.close()    