import sys
import signal
from pybleno import *

print "importing Characteristics"
from Characteristics import *
print "done importing Characteristics"

def onStateChange(state):
    print(state)
    if state == "poweredOn":
        bleno.startAdvertising("Spectrometer", ["dfdc"])
    else:
        bleno.stopAdvertising()

def onAdvertisingStart(error):
    if error:
        print(error)
    else:
        print "Configuring bleno services"
        bleno.setServices([
            BlenoPrimaryService({
                "uuid":"a1e1",
                "characteristics": [
                    IntegrationTime ("19b5"), 
                    Scans_to_average("20b4"), 
                    Laser_enable    ("7610"), 
                    Get_Spectra     ("1ac8")
                ]
            })
        ])

# instantiate Bleno and register callbacks
print "instantiating Bleno"
bleno = Bleno()
bleno.on("stateChange",      onStateChange)
bleno.on("advertisingStart", onAdvertisingStart)

# wait for user to press return?
print "Press <enter> to exit..."
if sys.version_info > (3, 0):
    input()
else:
    raw_input()

print "Closing Bleno"
bleno.stopAdvertising()
bleno.disconnect()

print("terminated")
sys.exit(1) # MZ: needed?
