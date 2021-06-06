from enum import Enum
from selve.communication import Command, CommandSingle
from selve.protocol import MethodCall, ServiceState, lightDigital, rainDigital, tempDigital, windDigital
from selve.protocol import ParameterType
from selve.protocol import DeviceType
from selve.protocol import CommandType
from selve.commands import Commands, CommeoCommandCommand, CommeoDeviceCommand, CommeoEventCommand, CommeoGroupCommand, CommeoParamCommand, CommeoSenSimCommand, CommeoSenderCommand, CommeoSensorCommand, CommeoServiceCommand
from selve.utils import singlemask
from selve.utils import true_in_list
from selve.utils import b64bytes_to_bitlist
import logging


_LOGGER = logging.getLogger(__name__)


class CommeoSenSimStore(Command):
    def __init__(self, deviceId, senSimId):
        super().__init__(CommeoSenSimCommand.STORE, [(ParameterType.INT, senSimId), (ParameterType.INT, deviceId)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])
class CommeoSenSimDelete(Command):
    def __init__(self, deviceId, senSimId):
        super().__init__(CommeoSenSimCommand.DELETE, [(ParameterType.INT, senSimId), (ParameterType.INT, deviceId)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])
class CommeoSenSimGetConfig(Command):
    def __init__(self, senSimId):
        super().__init__(CommeoSenSimCommand.GETCONFIG, [(ParameterType.INT, senSimId)])
    def process_response(self, methodResponse):
        self.name = str(methodResponse.parameters[0][1])
        self.senSimId = int(methodResponse.parameters[1][1])
        self.activity = bool(methodResponse.parameters[2][1])

class CommeoSenSimSetConfig(Command):
    def __init__(self, senSimId, activate):
        super().__init__(CommeoSenSimCommand.SETCONFIG, [(ParameterType.INT, senSimId), (ParameterType.INT, activate)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoSenSimSetLabel(Command):
    def __init__(self, senSimId, name):
        super().__init__(CommeoSenSimCommand.SETLABEL, [(ParameterType.INT, senSimId), (ParameterType.INT, name)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoSenSimSetValues(Command):
    def __init__(self, senSimId, windDigital, rainDigital, tempDigital, lightDigital, tempAnalog, windAnalog, sun1Analog, dayLightAnalog, sun2Analog, sun3Analog):
        super().__init__(CommeoSenSimCommand.SETVALUES, [(ParameterType.INT, senSimId), (ParameterType.INT, windDigital), (ParameterType.INT, rainDigital), (ParameterType.INT, tempDigital), (ParameterType.INT, lightDigital), (ParameterType.INT, tempAnalog), (ParameterType.INT, windAnalog), (ParameterType.INT, sun1Analog), (ParameterType.INT, dayLightAnalog), (ParameterType.INT, sun2Analog), (ParameterType.INT, sun3Analog)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoSenSimGetValues(CommandSingle):
    def __init__(self, senSimId):
        super().__init__(CommeoSenSimCommand.GETVALUES, senSimId)
    def process_response(self, methodResponse):
        self.windDigital = windDigital(int(methodResponse.parameters[1][1]))
        self.rainDigital = rainDigital(int(methodResponse.parameters[2][1]))
        self.tempDigital = tempDigital(int(methodResponse.parameters[3][1]))
        self.lightDigital = lightDigital(int(methodResponse.parameters[4][1]))
        self.tempAnalog = int(methodResponse.parameters[5][1])
        self.windAnalog = int(methodResponse.parameters[6][1])
        self.sun1Analog = int(methodResponse.parameters[7][1])
        self.dayLightAnalog = int(methodResponse.parameters[8][1])
        self.sun2Analog = int(methodResponse.parameters[9][1])
        self.sun3Analog = int(methodResponse.parameters[10][1])

class CommeoSenSimGetIDs(Command):
    def __init__(self, deviceId):
        super().__init__(CommeoSenSimCommand.GETIDS)
    def process_response(self, methodResponse):
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)

class CommeoSenSimFactory(CommandSingle):
    def __init__(self, senSimId):
        super().__init__(CommeoSenSimCommand.FACTORY, senSimId)
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoSenSimDrive(Command):
    def __init__(self, senSimId, command):
        super().__init__(CommeoSenSimCommand.DRIVE, [(ParameterType.INT, senSimId), (ParameterType.INT, command)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoSenSimSetTest(Command):
    def __init__(self, senSimId, testMode):
        super().__init__(CommeoSenSimCommand.SETTEST, [(ParameterType.INT, senSimId), (ParameterType.INT, testMode)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoSenSimGetTest(CommandSingle):
    def __init__(self, senSimId):
        super().__init__(CommeoSenSimCommand.GETTEST)
    def process_response(self, methodResponse):
        self.testMode = bool(methodResponse.parameters[1][1])
    