from pybleno import *
import sys, signal
from Characteristics import *
sys.path.append("/home/pi/code/Wasatch.PY/")

bleno = Bleno()

def onStateChange(state):
    print(state)
    if state == "poweredOn":
        bleno.startAdvertising("Spectrometer", ["dfdc"])
    else:
        bleno.stopAdvertising()
bleno.on("stateChange", onStateChange)
    
def onAdvertisingStart(error):
    print(error)
    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                "uuid":"a1e1",
                "characteristics":[IntegrationTime("19b5"), Scans_to_average("20b4"), Laser_enable("7610"), Get_Spectra("1ac8")]
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
