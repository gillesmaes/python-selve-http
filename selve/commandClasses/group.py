from selve.device import Device
from selve.protocol import CommunicationType, DeviceClass, DeviceCommandTypes, ParameterType
from build.lib.selve.utils import b64bytes_to_bitlist, true_in_list
import logging
from selve.commands import CommeoGroupCommand
from selve.communication import Command, CommandSingle
_LOGGER = logging.getLogger(__name__)


class CommeoGroupRead(CommandSingle):
    def __init__(self, groupId):
        super().__init__(CommeoGroupCommand.READ, groupId)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[1][1]))]
        _LOGGER.debug(self.ids)
        self.name = str(methodResponse.parameters[2][1])

class CommeoGroupWrite(Command):
    def __init__(self, groupId, actorIdMask, name):
        super().__init__(CommeoGroupCommand.WRITE, [(ParameterType.INT, groupId), (ParameterType.BASE64, actorIdMask), (ParameterType.STRING, name)])
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])

class CommeoGroupGetIDs(Command):
    def __init__(self):
        super().__init__(CommeoGroupCommand.GETIDS)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)

class CommeoGroupDelete(CommandSingle):
    def __init__(self, groupId):
        super().__init__(CommeoGroupCommand.DELETE, groupId)
    def process_response(self, methodResponse):
        super().process_response(methodResponse)
        self.executed = bool(methodResponse.parameters[0][1])

class GroupDevice(Device):
    def __init__(self, gateway, id, discover = False):
        super().__init__(gateway, id, discover)
        self.communicationType = CommunicationType.COMMEO
        self.deviceClass = DeviceClass.GROUP
        if discover:
            self.discover_properties()

    def discover_properties(self):
        try:
            command = CommeoGroupRead(self.ID)
            command.execute(self.gateway)
            self.device_type = "GROUP"
            self.name = command.name
            self.deviceClass = DeviceClass.GROUP
            self.communicationType = CommunicationType.COMMEO
        except Exception as e1:
            _LOGGER.exception ("not : " + str(e1))


    def readGroup(self, id):
        command = CommeoGroupRead(id)
        command.execute(self.gateway)
        return command

    def writeGroup(self, id, idMask, name):
        command = CommeoGroupWrite(id, idMask, name)
        command.execute(self.gateway)

    def deleteGroup(self, id):
        command = CommeoGroupDelete(id)
        command.execute(self.gateway)

