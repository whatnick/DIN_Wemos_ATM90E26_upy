# DIN_Wemos_ATM90E26_upy
Micropython code to run on the DIN rail dual ATM90E26 module.
* Web Front End from [@john_newall](https://twitter.com/john_newall).
Works on both ESP32 and ESP8266, better on ESP32 due to better RAM and CPU resources. Please read John's [excellent article](https://www.johnnewall.com/article/microcontroller-website-energy-monitor/) on web design with limited resources.

* Micropython Energy Monitor inspiration from [@shenki](https://twitter.com/shenki).
His [presentation at PyconAU2017](https://2017.pycon-au.org/schedule/presentation/69/) inspired me to make this port and dive into the wonderful world of Python on microcontrollers, FPGA's and everything else.
--------------------------
### Setup
If you would like to build your own micropython image please follow the ESP32 micropython instructions 
[here](https://github.com/micropython/micropython/blob/master/ports/esp32/README.md) or download a pre-built 
one [here](http://micropython.org/download#esp32).


### Loading code
For best performance this code uses a custom micropython image which can be obtained
[here](https://drive.google.com/file/d/0B7PX_Donnye2ZjB5cWd1X0NpOTFhQ29BT3pjdC1rYXdkRG5v/view). 
This image has picoweb and a few modules **frozen** to minimise runtime RAM footprint.
Flash this image and copy over the required Python, HTML, CSS and JS files for the web application
using the serial thunking approach developed by [mpy-utils](https://github.com/nickzoic/mpy-utils).
The **mpy-fuse** is particularly useful for copying over the large selection of files which form this project.

### Running
The code base is composed of multiple runnable python files. The main.py is designed to get basic functionality going,
 additional experiments can be performed by pressing **Ctrl+C** in the micropython console and switching to another main 
 function.
 
### IoT Servers
The sample code here is targeted to self-hosted (Graphite)[http://graphite.readthedocs.io/en/latest/install.html]. Recommended methon of installing and running with all the dependencies in place is docker image.
