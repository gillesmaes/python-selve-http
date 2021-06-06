from enum import EnumMeta
from selve.communication import *


from selve.protocol import *
from selve.commands import *
from selve.utils import *
import logging
_LOGGER = logging.getLogger(__name__)


class CommeoCommandDevice(Command):
    def __init__(self, deviceId, command, commmandType = DeviceCommandTypes.MANUAL, parameter = 0):
        super().__init__(CommeoCommandCommand.DEVICE, [(ParameterType.INT, deviceId), (ParameterType.INT, command), (ParameterType.INT, commmandType), (ParameterType.INT, parameter)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoCommandGroup(Command):
    def __init__(self, deviceId, command, commmandType = DeviceCommandTypes.MANUAL, parameter = 0):
        super().__init__(CommeoCommandCommand.GROUP, [(ParameterType.INT, deviceId), (ParameterType.INT, command), (ParameterType.INT, commmandType), (ParameterType.INT, parameter)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoCommandGroupMan(Command):
    def __init__(self, command, commandType, deviceIdMask, parameter = 0):
        super().__init__(CommeoCommandCommand.GROUPMAN, [(ParameterType.INT, command), (ParameterType.INT, commandType), (ParameterType.BASE64, deviceIdMask), (ParameterType.INT, parameter)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)

class CommeoCommandResult(Command):
    def __init__(self):
        super().__init__(CommeoCommandCommand.RESULT)
    def process_response(self, methodResponse):
        self.command = DeviceCommands(int(methodResponse.parameters[0][1]))
        self.commandType = DeviceCommandTypes(int(methodResponse.parameters[1][1]))
        self.executed = bool(methodResponse.parameters[2][1])
        self.successIds = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[3][1]))]
        self.failedIds = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[4][1]))]
