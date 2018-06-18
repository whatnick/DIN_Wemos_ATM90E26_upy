import picoweb
from wifiConnect import do_connect

ip = do_connect('blynkspot','blynkpass')
 
app = picoweb.WebApp(__name__)
 
@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from resp.awrite("Hello world from picoweb running on the ESP32")
 
app.run(debug=True, host = ip)
