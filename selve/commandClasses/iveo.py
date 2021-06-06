from enum import Enum

from selve.protocol import MethodCall
from selve.protocol import ParameterType
from selve.protocol import DeviceType
from selve.protocol import CommandType
from selve.commands import Commands, IveoCommand
from selve.communication import Command, CommandMask, CommandSingle
from selve.utils import singlemask
from selve.utils import true_in_list
from selve.utils import b64bytes_to_bitlist
import logging


_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

    
class IveoCommandFactory(CommandSingle):

    def __init__(self, iveoID):
        super().__init__(IveoCommand.FACTORY, iveoID)

class IveoCommandTeach(CommandSingle):
    def __init__(self, iveoID):
        super().__init__(IveoCommand.TEACH, iveoID)

    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])   

class IveoCommandLearn(CommandSingle):
    def __init__(self, iveoID):
        super().__init__(IveoCommand.LEARN, iveoID)
    
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1]) 
         
class IveoCommandManual(CommandMask):
    def  __init__(self, mask, command):
        super().__init__(IveoCommand.MANUAL, mask, command)
    
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1]) 

class IveoCommandAutomatic(CommandMask):
    def  __init__(self, mask, command):
        super().__init__(IveoCommand.AUTOMATIC, mask, command)
    
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class IveoCommandResult(MethodCall):
    def __init__(self, command, mask, state):
        super().__init__(IveoCommand.RESULT, [(ParameterType.INT, command), (ParameterType.BASE64, mask), (ParameterType.INT, state)])

class IveoCommandSetLabel(Command):
    def __init__(self, iveoId, label):
        super().__init__(IveoCommand.SETLABEL, [(ParameterType.INT, iveoId), (ParameterType.STRING, label)])

    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class IveoCommandSetConfig(Command):
    def __init__(self, iveoId, activity, device_type):
        super().__init__(IveoCommand.SETCONFIG, [(ParameterType.INT, iveoId), (ParameterType.INT, activity), (ParameterType.INT, device_type)])
    
    def process_response(self, methodResponse):
        self.executed = bool(methodResponse.parameters[0][1])

class IveoCommandGetConfig(CommandSingle):
    def __init__(self, iveoId):
        super().__init__(IveoCommand.GETCONFIG, iveoId)
    
    def process_response(self, methodResponse):
        self.name = methodResponse.parameters[0][1]
        self.activity = methodResponse.parameters[2][1]
        self.deviceType = DeviceType(int(methodResponse.parameters[3][1]))

class IveoCommandGetIds(Command):
    def __init__(self):
        super().__init__(IveoCommand.GETIDS)
    
    def process_response(self, methodResponse):
        self.ids = [ b for b in true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))]
        _LOGGER.debug(self.ids)

class IveoDevice():

    def __init__(self, gateway, iveoID, discover = False):
        self.iveoID = iveoID
        self.gateway = gateway
        self.mask = singlemask(iveoID)
        self.device_type = DeviceType.UNKNOWN
        self.name = "Not defined"
        if discover:
            self.discover_properties()
    
    def stop(self, automatic = False):
        self.executeCommand(CommandType.STOP, automatic)

    def moveDown(self, automatic = False):
        self.executeCommand(CommandType.DEPARTURE, automatic)
    
    def moveUp(self, automatic = False):
        self.executeCommand(CommandType.DRIVEAWAY, automatic)
    
    def moveIntermediatePosition1(self, automatic = False):
        self.executeCommand(CommandType.POSITION_1, automatic)

    def moveIntermediatePosition2(self, automatic = False):
        self.executeCommand(CommandType.POSITION_2, automatic)
    
    def learnChannel(self, channel):
        command = IveoCommandLearn(self.iveoID)
        command.execute(self.gateway)
        if command.executed:
            _LOGGER.info("Device with id " + str(self.iveoID) + " learning")
            self.gateway.teach_channel(channel)

    def executeCommand(self, commandType, automatic = False):
        if automatic:
            command = IveoCommandAutomatic(self.mask, commandType)
        else:
            command = IveoCommandManual(self.mask, commandType)
        command.execute(self.gateway)
        return command

    def discover_properties(self):
        command = IveoComandGetConfig(self.iveoID)
        command.execute(self.gateway)
        self.device_type = command.deviceType
        self.name = command.name
    
    def __str__(self):
        return "Device of type: " + self.device_type.name + " on channel " + str(self.iveoID) + " with name " + self.name