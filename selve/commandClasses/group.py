from enum import Enum
from selve.communication import Command, CommandSingle
from selve.protocol import MethodCall, ServiceState
from selve.protocol import ParameterType
from selve.protocol import DeviceType
from selve.protocol import CommandType
from selve.commands import Commands, CommeoCommandCommand, CommeoDeviceCommand, CommeoEventCommand, CommeoGroupCommand, CommeoParamCommand, CommeoSenSimCommand, CommeoSenderCommand, CommeoSensorCommand, CommeoServiceCommand
from selve.utils import singlemask
from selve.utils import true_in_list
from selve.utils import b64bytes_to_bitlist
import logging
_LOGGER = logging.getLogger(__name__)


class CommeoGroupRead(CommandSingle):
    def __init__(self, groupId):
        super().__init__(CommeoGroupCommand.READ, groupId)
    def process_response(self, methodResponse):
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[1][1]))]
        _LOGGER.debug(self.ids)
        self.name = str(methodResponse.parameters[2][1])

class CommeoGroupWrite(Command):
    def __init__(self, groupId, actorIdMask, name):
        super().__init__(CommeoGroupCommand.WRITE, [(ParameterType.INT, groupId), (ParameterType.BASE64, actorIdMask), (ParameterType.STRING, name)])
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoGroupGetIDs(Command):
    def __init__(self, groupId):
        super().__init__(CommeoGroupCommand.GETIDS)
    def process_response(self, methodResponse):
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)

class CommeoGroupDelete(CommandSingle):
    def __init__(self, groupId):
        super().__init__(CommeoGroupCommand.DELETE, groupId)
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

