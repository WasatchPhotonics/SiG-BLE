from pybleno import Characteristic
import array, sys, logging
sys.path.append("/home/pi/code/Wasatch.PY/")
import json
from wasatch.WasatchDevice import WasatchDevice
from wasatch.WasatchBus import WasatchBus
from wasatch import applog

log = logging.getLogger(__name__)
logger = applog.MainLogger("DEBUG")

log.debug("instantiating WasatchBus")
bus = WasatchBus(use_sim = False)

if not bus.devices:
    print("No Wasatch USB spectrometers found.")
    sys.exit(0)

uid = bus.devices[0]
log.debug("instantiating WasatchDevice (blocking)")
device = WasatchDevice(uid, bus_order=0)
ok = device.connect()
log.info("connect: device connected")
device.change_setting("integration_time_ms", 10)


class IntegrationTime(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(self, {'uuid': uuid, 'properties': ['read', 'write'], 'value': None})
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
        
    def onReadRequest(self, offset, callback):
        #print(offset, callback, self._value)
        callback(Characteristic.RESULT_SUCCESS, self._value)
        
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        device.change_setting("integration_time_ms", data)
        print("Integration time changed to %d ms" %int(data))
        if self._updateValueCallback:
            self._updateValueCallback(self._value)
        callback(Characteristic.RESULT_SUCCESS)
    
    def onSubscribe(self, maxValueSize, updateValueCallback):
        print("onSubscribe")
        self._updateValueCallback = updatevalueCallback
        
    def onUnsubscribe(self):
        print("on unsubscribe")
        self._updateValueCallback = None
            
class Scans_to_average(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(self, {'uuid': uuid, 'properties': ['read', 'write'], 'value': None})
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
        
    def onReadRequest(self, offset, callback):
        print()
        callback(Characteristic.RESULT_SUCCESS, self._value)
    
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        device.change_setting("scans_to_average", data)
        print("Scans average changed to %d" %int(data))
        if self._updateValueCallback:
            self._updateValueCallback(self._value)
        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print("onSubscribe")
        self._updateValueCallback = updatevalueCallback
        
    def onUnsubscribe(self):
        print("on unsubscribe")
        self._updateValueCallback = None
                  
class Get_Spectra(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(self, {'uuid': uuid, 'properties': ['read'], 'value': None})
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
        
    def onReadRequest(self, offset, callback):
        #print(self._value, self.value, callback, offset)
        reading = device.acquire_data()
        print(sys.getsizeof(json.dumps(reading.spectrum)))
        self._value = bytearray(b'768')
        callback(Characteristic.RESULT_SUCCESS, self._value)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print("onSubscribe")
        self._updateValueCallback = updatevalueCallback
        
    def onUnsubscribe(self):
        print("on unsubscribe")
        self._updateValueCallback = None
                  
class Laser_enable(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(self, {'uuid': uuid, 'properties': ['read', 'write'], 'value': None})
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
        
    def onReadRequest(self, offset, callback):
        print()
        callback(Characteristic.RESULT_SUCCESS, self._value)
    
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        if data:
            device.change_setting("laser_enable", bool(data))
            print("Laser enabled" %int(data))
        else:
            device.change_setting("laser_enable", bool(data))
            print("Laser disabled" %int(data))
        if self._updateValueCallback:
            self._updateValueCallback(self._value)
        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print("onSubscribe")
        self._updateValueCallback = updatevalueCallback
        
    def onUnsubscribe(self):
        print("on unsubscribe")
        self._updateValueCallback = None
    