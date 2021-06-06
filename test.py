import selve
from selve import Gateway

portname = '/dev/virtual-tty'
gat = Gateway(portname, False)
gat.discover()
devices = list(gat.devices.values())