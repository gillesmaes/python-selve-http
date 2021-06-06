from enum import Enum

from selve.protocol import DayMode, DeviceState, MethodCall, MovementState, ScanState, ServiceState
from selve.protocol import ParameterType
from selve.protocol import DeviceType
from selve.protocol import CommandType
from selve.commands import Commands, CommeoCommandCommand, CommeoDeviceCommand, CommeoEventCommand, CommeoGroupCommand, CommeoParamCommand, CommeoSenSimCommand, CommeoSenderCommand, CommeoSensorCommand, CommeoServiceCommand
from selve.utils import intToBoolarray, singlemask, valueToPercentage
from selve.utils import true_in_list
from selve.utils import b64bytes_to_bitlist
from selve.communication import Command, CommandSingle
import logging
_LOGGER = logging.getLogger(__name__)



class CommeoDeviceScanStart(Command):
    def __init__(self):
        super().__init__(CommeoDeviceCommand.SCANSTART)
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])
class CommeoDeviceScanStop(Command):
    def __init__(self):
        super().__init__(CommeoDeviceCommand.SCANSTOP)
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])
class CommeoDeviceScanResult(Command):
    def __init__(self):
        super().__init__(CommeoDeviceCommand.SCANRESULT)
    def process_response(self, methodResponse):
        self.scanState = ScanState(int(methodResponse.parameters[0][1]))
        self.noNewDevices = int(methodResponse.parameters[1][1])
        self.foundIds = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[2][1]))]

class CommeoDeviceSave(CommandSingle):
    def __init__(self, deviceId):
        super().__init__(CommeoDeviceCommand.SAVE, deviceId)
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoDeviceGetIDs(Command):
    def __init__(self):
        super().__init__(CommeoDeviceCommand.GETIDS)

    def process_response(self, methodResponse):
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)

class CommeoDeviceGetInfo(CommandSingle):
    def __init__(self, deviceId):
        super().__init__(CommeoDeviceCommand.GETINFO, deviceId)

    def process_response(self, methodResponse):
        self.name = methodResponse.parameters[0][1]
        self.rfAddress = methodResponse.parameters[2][1]
        self.deviceType = DeviceType(int(methodResponse.parameters[3][1]))
        self.state = DeviceState(int(methodResponse.parameters[4][1]))

class CommeoDeviceGetValues(CommandSingle):
    def __init__(self, deviceId):
        super().__init__(CommeoDeviceCommand.GETVALUES, deviceId)


    def process_response(self, methodResponse):
        self.name = methodResponse.parameters[0][1]
        self.movementState = MovementState(int(methodResponse.parameters[2][1]))
        self.value = valueToPercentage(int(methodResponse.parameters[3][1]))
        self.targetValue = valueToPercentage(int(methodResponse.parameters[4][1]))

        bArr = intToBoolarray(int(methodResponse.parameters[5][1]))
        self.unreachable = bArr[0]
        self.overload = bArr[1]
        self.obstructed = bArr[2]
        self.alarm = bArr[3]
        self.lostSensor = bArr[4]
        self.automaticMode = bArr[5]
        self.gatewayNotLearned = bArr[6]
        self.windAlarm = bArr[7]
        self.rainAlarm = bArr[8]
        self.freezingAlarm = bArr[9]
        
        self.dayMode = DayMode(int(methodResponse.parameters[6][1]))

class CommeoDeviceSetFunction(Command):
    def __init__(self, deviceId, function):
        super().__init__(CommeoDeviceCommand.SETFUNCTION, [(ParameterType.INT, deviceId), (ParameterType.INT, function)])

    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoDeviceSetLabel(Command):
    def __init__(self, deviceId, name):
        super().__init__(CommeoDeviceCommand.SETLABEL, [(ParameterType.INT, deviceId), (ParameterType.STRING, name)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoDeviceSetType(Command):
    def __init__(self, deviceId, type):
        super().__init__(CommeoDeviceCommand.SETTYPE, [(ParameterType.INT, deviceId), (ParameterType.INT, type)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoDeviceDelete(CommandSingle):
    def __init__(self, deviceId):
        super().__init__(CommeoDeviceCommand.DELETE, deviceId)

    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])
    
class CommeoDeviceWriteManual(Command):
    def __init__(self, deviceId, rfAddress, name, deviceType):
        super().__init__(CommeoDeviceCommand.WRITEMANUAL, [(ParameterType.STRING, name), (ParameterType.INT, deviceId), (ParameterType.INT, rfAddress), (ParameterType.INT, deviceType)])

    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])