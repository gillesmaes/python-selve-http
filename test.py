import logging
import sys
from time import sleep
from selve import utils
from selve.protocol import CommandType, CommandTypeIveo
from selve.utils import bitstring_to_bytes
from selve.commandClasses.iveo import IveoCommandAutomatic, IveoDevice
import selve
from selve import Gateway



portname = '/dev/ttyUSB0'
gat = Gateway(portname, False)
gat._LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
gat._LOGGER.addHandler(handler)

gat.setEvents(0,0,0,1,1)
gat.getEvents()


gat.discover()
devices = list(gat.devices.values())

t1 = utils.multimask([0,1,2,3,4,5])

ttt = utils.b64bytes_to_bitlist(t1)

gat.pingGateway()

#gat.readThread.join()
#gat.writeThread.join()

#gat.devices[1].executeCommand(CommandTypeIveo.DRIVEDOWN, True)
#gat.devices[4].executeCommand(CommandTypeIveo.DRIVEUP, True)
#gat.devices[5].executeCommand(CommandTypeIveo.DRIVEUP, True)

gat.addDevice(3, IveoDevice(gat, 3, False))
gat.devices[3].learnGatewayIn()

devices = gat.scanActorDevices()
gat.saveActorDevices(devices)
