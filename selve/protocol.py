
from enum import Enum
from itertools import chain
from serial.serialutil import STOPBITS_ONE
import untangle
import logging


_LOGGER = logging.getLogger(__name__)
class DeviceType(Enum):
    UNKNOWN = 0
    SHUTTER = 1
    BLIND = 2
    AWNING = 3
    SWITCH = 4
    DIMMER = 5
    NIGHT_LIGHT = 6
    DRAWN_LIGHT = 7
    HEATING = 8
    COOLING = 9
    COOLING2 = 10
    GATEWAY = 11

class DeviceState(Enum):
    UNUSED = 0
    USED = 1
    TEMPORARY = 2
    STALLED = 3

class MovementState(Enum):
    UNKOWN = 0
    STOPPED_OFF = 1
    UP_ON = 2
    DOWN_ON = 3

class CommunicationType(Enum):
    COMMMEO = 0
    IVEO = 1
    UNKNOWN = 99

class CommandType(Enum):
    STOP = 0
    DRIVEAWAY = 1
    DEPARTURE = 2
    POSITION_1 = 3
    POSITION_2 = 4

class DeviceCommands(Enum):
    STOP = 0
    DRIVEUP = 1
    DRIVEDOWN = 2
    DRIVEPOS1 = 3
    SAVEPOS1 = 4
    DRIVEPOS2 = 5
    SAVEPOS2 = 6
    DRIVEPOS = 7
    STEPUP = 8
    STEPDOWN = 9 
    AUTOON = 10
    AUTOOFF = 11

class DeviceCommandTypes(Enum):
    FORCED = 0
    MANUAL = 1
    TIME = 2
    GLASS = 3

class SenSimCommands(Enum):
    STOP = 0
    UP = 1
    DOWN = 2
    POS1 = 3
    POS2 = 5

class ParameterType(Enum):
    INT = "int"
    STRING = "string"
    BASE64 = "base64"

class ScanState(Enum):
    IDLE = 0
    RUN = 1
    VERIFY = 2
    END_SUCCESS = 3
    END_FAILED = 4

class TeachState(Enum):
    IDLE = 0
    RUN = 1
    END_SUCCESS = 2

class ServiceState(Enum):
    BOOTLOADER = 0
    UPDATE = 1
    STARTUP = 2
    READY = 3

class SensorState(Enum):
    INVALID = 0
    AVAILABLE = 1
    LOW_BATTERY = 2
    COMMUNICATION_LOSS = 3
    TESTMODE = 4
    SERVICEMODE = 5

class LEDMode(Enum):
    OFF = 0
    ON = 1

class Forwarding(Enum):
    OFF = 0
    ON = 1

class DutyMode(Enum):
    NOT_BLOCKED = 0
    BLOCKED = 1

class DayMode(Enum):
    UNKOWN = 0
    NIGHTMODE = 1
    DAWNING = 2
    DAY = 3
    DUSK = 4

class deviceFunctions(Enum):
    SELECT = 0
    INSTALL = 1
    SENSOR = 2
    MANPROG = 3
    AUTOPROG = 4
    STOREPOSITION = 5
    DRIVEUP = 6
    DRIVEDOWN = 7
    KEYRELEASE = 8
    DRIVESTOP = 9

class LogType(Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2

## SensorVariables ##

class windDigital(Enum):
    NONE = 0
    NO_ALARM = 1
    ALARM = 2

class rainDigital(Enum):
    NONE = 0
    NO_ALARM = 1
    ALARM = 2

class tempDigital(Enum):
    NONE = 0
    NORMAL = 1
    FREEZING = 2
    HEAT = 3

class lightDigital(Enum):
    NONE = 0
    DARK = 1
    DAWN = 2
    NORMAL = 3
    LIGHT = 4

## senderEvents ##

class senderEvents(Enum):
    UNKNOWN = 0
    DRIVEUP = 1
    DRIVEDOWN = 2
    STOP = 3
    POS1 = 4
    POS2 = 5
    SAVEPOS1 = 6
    SAVEPOS2 = 7
    AUTO = 8
    MAN = 9
    NAME = 10
    KEYRELEASE = 11
    SELECT = 12
    DELETE = 13

class MethodCall:

    def __init__(self, method_name, parameters = []):
        self.method_name = method_name
        self.parameters = parameters

    def serializeToXML(self):
        xmlstr = "<methodCall>"
        xmlstr += "<methodName>"+self.method_name+"</methodName>"
        if (len(self.parameters) > 0):
            xmlstr += "<array>"
            for typ, val in self.parameters:
                xmlstr+="<{0}>{1}</{0}>".format(typ.value, val)
            xmlstr += "</array>"
        xmlstr+= "</methodCall>"
        return xmlstr.encode('utf-8')
    
    def execute(self, gateway):
        response = gateway.executeCommand(self)
        if response != None and isinstance(response, MethodResponse):
            self.process_response(response)
    
    def process_response(self, methodResponse):
        _LOGGER.debug(methodResponse)


class MethodResponse:

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

class ErrorResponse:

    def __init__(self, message, code):
        self.message = message
        self.code = code


def create_error(obj):
    return ErrorResponse(obj.methodResponse.fault.array.string.cdata, obj.methodResponse.fault.array.int.cdata ) 

def create_response(obj):
    array = obj.methodResponse.array
    methodName = list(array.string)[0].cdata
    str_params_tmp = list(array.string)[1:]
    str_params = [(ParameterType.STRING, v.cdata) for v in str_params_tmp]
    int_params = []
    if hasattr(array, ParameterType.INT.value):
        int_params = [(ParameterType.INT, v.cdata) for v in list(array.int)]
    b64_params = []
    if hasattr(array, ParameterType.BASE64.value):
        b64_params = [(ParameterType.BASE64, v.cdata) for v in list(array.base64)]
    paramslist = [str_params, int_params, b64_params]
    flat_params_list = list(chain.from_iterable(paramslist))
    return MethodResponse(methodName, flat_params_list)


def process_response(xmlstr):
    _LOGGER.debug(str(xmlstr))
    #The selve device sometimes answers a badformed header. This is a patch
    xmlstr = str(xmlstr).replace('<?xml version="1.0"? encoding="UTF-8">', '<?xml version="1.0" encoding="UTF-8"?>')
    
    res = untangle.parse(xmlstr)
    if not hasattr(res, 'methodResponse'):
        _LOGGER.error("Bad response format")
        return None
    if hasattr(res.methodResponse, 'fault'):
        return create_error(res)
    return create_response(res)

def main():

    selve_string = u'''<?xml version="1.0"? encoding="UTF-8">
    <methodResponse>
        <array>
            <string>Methodenname</string>
            <string>Parameter 1</string>
            <int>Parameter 2</int>
            <base64>Parameter 3</base64>
        </array>
    </methodResponse>
    '''

    error_string = '''<?xml version="1.0" encoding="UTF-8"?>
    <methodResponse>
        <fault>
            <array>
                <string>Method not supported!</string>                
                <int>2</int>                
            </array>
        </fault>
    </methodResponse>
    '''

    a ='<?xml version="1.0" encoding="UTF-8"?>\r\n<methodResponse>\r\n\t<array>\r\n\t\t<string>selve.GW.iveo.getIDs</string>\r\n\t\t<base64>fx4AAAAAAAA=</base64>\r\n\t</array>\r\n</methodResponse>\r\n\n'

    process_response(selve_string)


if __name__ == '__main__':
    main()
