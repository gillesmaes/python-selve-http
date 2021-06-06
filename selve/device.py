from selve.commandClasses.device import CommeoDeviceGetValues
from selve.commandClasses.iveo import IveoCommandGetConfig, IveoCommandGetIds
from build.lib.selve import communication
from selve.utils import *
from selve.communication import *
import logging
_LOGGER = logging.getLogger(__name__)

class Device():

    def __init__(self, gateway, ID, communicationType, discover = False):
        self.ID = ID
        self.gateway = gateway
        self.mask = singlemask(ID)
        self.device_type = DeviceType.UNKNOWN
        self.communicationType = communicationType
        self.name = "Not defined"
        if discover:
            self.discover_properties()
    
    def executeCommand(self, commandType, automatic = False):
        if automatic:
            command = CommeoDeviceCommand(self.mask, commandType)
        else:
            command = CommeoDeviceCommand(self.mask, commandType)
        command.execute(self.gateway)
        return command

    def discover_properties(self):
        if self.communicationType == CommunicationType.COMMMEO:
            try:
                command = CommeoDeviceGetValues
            except Exception as e1:
                _LOGGER.exception ("not : " + str(e1))


        elif self.communicationType == CommunicationType.IVEO:
            command = IveoCommandGetConfig(self.ID)
            command.execute(self.gateway)
            self.device_type = command.deviceType
            self.name = command.name
            self.activity = command.activity

        else:
            pass
        

    ## Actor ##


    ## Sensor ##


    ## SenSim ##


    ## Sender ##


    ## Iveo ##


    

    
    def __str__(self):
        return "Device " + self.device_type.name + " of type: " + self.communicationType + " on channel " + str(self.ID) + " with name " + self.name