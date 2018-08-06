from pybleno import *
import sys, signal
from int_time_ms import *
sys.path.append("/home/pi/code/Wasatch.PY/")

bleno = Bleno()

def onStateChange(state):
    print(state)
    if state == "poweredOn":
        bleno.startAdvertising("Integaration_time_ms", ["dfdc"])
    else:
        bleno.stopAdvertising()
bleno.on("stateChange", onStateChange)
    
def onAdvertisingStart(error):
    print(error)
    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                "uuid":"a1e1",
                "characteristics":[IntegrationTime("19b5")
                                   ]
                })
            ])
bleno.on("advertisingStart", onAdvertisingStart)

if sys.version_info > (3, 0):
    input()
else:
    raw_input()
bleno.stopAdvertising()
bleno.disconnect()

print("terminated")

sys.exit(1)
    