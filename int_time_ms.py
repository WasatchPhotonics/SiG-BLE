from pybleno import Characteristic
import array, sys
sys.path.append("/home/pi/code/Wasatch.PY/")
from demo import WasatchDemo

spec = WasatchDemo()
spec.connect()
class IntegrationTime(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(self, {'uuid': uuid, 'properties': ['read', 'write'], 'value': None})
        self._value = array.array("B", [0]*0)
        self._updateValueCallback = None
        
    def onReadRequest(self, offset, callback):
        print()
        callback(Characteristic.RESULT_SUCCESS, self._value)
        
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        spec.device.change_setting("integration_time_ms", data)
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
            

