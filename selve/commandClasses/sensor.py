from enum import Enum
from os import name
from selve.communication import Command, CommandSingle
from selve.protocol import MethodCall, SensorState, ServiceState, TeachState, lightDigital, rainDigital, tempDigital, windDigital
from selve.protocol import ParameterType
from selve.protocol import DeviceType
from selve.protocol import CommandType
from selve.commands import Commands, CommeoCommandCommand, CommeoDeviceCommand, CommeoEventCommand, CommeoGroupCommand, CommeoParamCommand, CommeoSenSimCommand, CommeoSenderCommand, CommeoSensorCommand, CommeoServiceCommand
from selve.utils import singlemask
from selve.utils import true_in_list
from selve.utils import b64bytes_to_bitlist
import logging

_LOGGER = logging.getLogger(__name__)

 
class CommeoSensorTechStart(Command):
    def __init__(self):
        super().__init__(CommeoSensorCommand.TEACHSTART)
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])
class CommeoSensorTeachStop(Command):
    def __init__(self):
        super().__init__(CommeoSensorCommand.TEACHSTOP)
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])
class CommeoSensorTeachResult(Command):
    def __init__(self):
        super().__init__(CommeoSensorCommand.TEACHRESULT)
    def process_response(self, methodResponse):
        self.teachState = TeachState(int(methodResponse.parameters[0][1]))
        self.timeLeft = int(methodResponse.parameters[1][1])
        self.foundId = int(methodResponse.parameters[2][1])

class CommeoSensorGetIDs(Command):
    def __init__(self):
        super().__init__(CommeoSensorCommand.GETIDS)

    def process_response(self, methodResponse):
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)

class CommeoSensorGetInfo(Command):
    def __init__(self):
        super().__init__(CommeoSensorCommand.GETINFO)

    def process_response(self, methodResponse):
        self.name = methodResponse.parameters[0][1]
        self.rfAddress = methodResponse.parameters[2][1]

class CommeoSensorGetValues(Command):
    def __init__(self, commeoId):
        super().__init__(CommeoSensorCommand.GETVALUES)


    def process_response(self, methodResponse):
        self.windDigital = windDigital(int(methodResponse.parameters[1][1]))
        self.rainDigital = rainDigital(int(methodResponse.parameters[2][1]))
        self.tempDigital = tempDigital(int(methodResponse.parameters[3][1]))
        self.lightDigital = lightDigital(int(methodResponse.parameters[4][1]))
        self.sensorState = SensorState(int(methodResponse.parameters[5][1]))
        self.tempAnalog = int(methodResponse.parameters[6][1])
        self.windAnalog = int(methodResponse.parameters[7][1])
        self.sun1Analog = int(methodResponse.parameters[8][1])
        self.dayLightAnalog = int(methodResponse.parameters[9][1])
        self.sun2Analog = int(methodResponse.parameters[10][1])
        self.sun3Analog = int(methodResponse.parameters[11][1])
        

class CommeoSensorSetLabel(Command):
    def __init__(self, deviceId, name):
        super().__init__(CommeoSensorCommand.SETLABEL, [(ParameterType.INT, deviceId), (ParameterType.STRING, name)])

    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoSensorDelete(CommandSingle):
    def __init__(self, deviceId):
        super().__init__(CommeoSensorCommand.DELETE, deviceId)

    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoSensorWriteManual(Command):
    def __init__(self, deviceId, address, name):
        super().__init__(CommeoSensorCommand.WRITEMANUAL, [(ParameterType.INT, deviceId), (ParameterType.INT, address), (ParameterType.STRING, name)])
    
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])