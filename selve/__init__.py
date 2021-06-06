#!/usr/bin/python

from selve.device import Device
import time
import serial
from enum import Enum
import logging
import threading
import queue

from selve.commandClasses.command import *
from selve.commandClasses.common import *
from selve.commandClasses.device import *
from selve.commandClasses.group import *
from selve.commandClasses.iveo import *
from selve.commandClasses.sender import *
from selve.commandClasses.senSim import *
from selve.commandClasses.sensor import *
from selve.communication import *
from selve.utils import * 
from selve.protocol import *



_LOGGER = logging.getLogger(__name__)

class Gateway():   

    def __init__(self, port, discover = True):
        """                
        Arguments:
            port {String} -- Serial port string as it is used in pyserial
        
        Keyword Arguments:
            discover {bool} -- True if the gateway should try to discover 
                               the devices on init (default: {True})
        """
        self.port = port
        self.connected = False
        self.inputQueue = queue.Queue()
        self.outputQueue = queue.Queue()

        _LOGGER.debug('check')
        
        try:
            self.configserial()

        except Exception as e:            
            _LOGGER.error ('error open serial port: ' + str(e))
            exit()

        if discover:
            self.discover()

        self.readThread = threading.Thread(target=self.readFromPort)
        self.readThread.start()

        self.writeThread = threading.Thread(target=self.writePort)
        self.writeThread.start()
    
    def configserial(self):
        """
        Configure the serial port
        """
        self.ser = serial.Serial(
            port=self.port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        self.ser.timeout = 0
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2

    def handleData(data):
        incomingEvent(str(data))

    def readFromPort(self):
        while True:
            response_str = "" 
            if self.ser.isOpen():
                if int(self.ser.in_waiting) > 0:                        
                    response = self.ser.readline().strip()
                    response_str += response.decode()
                    _LOGGER.info('read data: ' + response_str)
                    if (response.decode() == ''):
                        self.handleData(response_str)

                
    def writePort(self):
        while True:
            response_str = "" 
            if self.outputQueue.not_empty:                        
                if self.ser.isOpen():
                    try:
                        self.ser.flushInput()
                        self.ser.flushOutput()
                        
                        self.ser.write(self.outputQueue.get())
                        time.sleep(0.5)
                        response_str = "" 
                        while True:
                            response = self.ser.readline().strip()
                            response_str += response.decode()
                            if (response.decode() == ''):
                                break
                            
                        self.ser.close()
                        _LOGGER.info('read data: ' + response_str)
                        #return process_response(response_str)
                        # handle response somehow here
                    except Exception as e1:
                        _LOGGER.exception ("error communicating...: " + str(e1))
                else:
                    _LOGGER.error ("cannot open serial port THREAD")
        



    def executeCommand(self, command):
        """[summary]
        Execute the given command using the serial port.
        It opens a communication to the serial port each time a
        command is executed.
        At this moment it doesn't keep a queue of commands. If
        a command blocks the serial it will wait.
        
        Arguments:
            command {protocol.MethodCall} -- Command to be send 
            through the serial port
        
        Returns:
            MethodResponse -- if the command was executed 
            sucessufully
            ErrorResponse -- if the gateway returns an error
        """
        commandstr = command.serializeToXML()
        _LOGGER.info('Gateway writting: ' + str(commandstr))

        if self.ser.isOpen():
            try:
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
                
                self.ser.write(commandstr)
                time.sleep(0.5)
                response_str = "" 
                while True:
                    response = self.ser.readline().strip()
                    response_str += response.decode()
                    if (response.decode() == ''):
                        break
                    
                self.ser.close()
                _LOGGER.info('read data: ' + response_str)
                return process_response(response_str)
            except Exception as e1:
                _LOGGER.exception ("error communicating...: " + str(e1))
        else:
            _LOGGER.error ("cannot open serial port")
        
        return None

    def discover(self):
        """[summary]
            Discover all devices registered on the usb-commeo        
        """
        commandIveo = IveoCommandGetIds()
        commandCommeo = CommeoDeviceGetIDs()
        num_retries = 5
        retry_n = 0
        retry_m = 0
        while not hasattr(commandIveo, "ids") and retry_n <=num_retries:
            commandIveo.execute(self)
            retry_n += 1
            time.sleep(1)
        while not hasattr(commandCommeo, "ids") and retry_m <=num_retries:
            commandCommeo.execute(self)
            retry_m += 1
            time.sleep(1)


        self.devices = {}
        if not hasattr(commandIveo, "ids"):
            _LOGGER.info("Associated Iveo Devices not found") 
            iveoDevices = {}
        else:
            _LOGGER.debug(f'discover ids: {commandIveo.ids}')
            iveoDevices = dict([(id, Device(self, id , True) )for id in commandIveo.ids])
        
        if not hasattr(commandCommeo, "ids"):
            _LOGGER.info("Associated Commeo Devices not found") 
            commeoDevices = {}
        else:
            _LOGGER.debug(f'discover ids: {commandCommeo.ids}')
            commeoDevices = dict([(id, Device(self, id , True) )for id in commandCommeo.ids])
        

        self.devices = iveoDevices | commeoDevices
        
        self.list_devices() 
       

    def is_id_registered(self, id):
        """[summary]
        check if a device id is registered on the gateway
        Arguments:
            id {int} -- Device id to check
        
        Returns:
            boolean -- True if the id is registered
                       False otherwise
        """
        return id in self.devices
        
    def list_devices(self):
        """[summary]
        Print the list of registered devices
        """ 
        for id, device in self.devices.items():
            print(str(device))
            #_LOGGER.info(str(device))
            
    def teach_channel(self, channel):
        command = IveoCommandTeach(channel)
        _LOGGER.info("Trying to teach channel " + str(channel))
        command.execute(self)
        if command.executed:
            _LOGGER.info("Channel " + str(channel) + "sucessfully teach" )

if __name__ == '__main__':
    #print (singlemask(2).decode('utf-8'))
    _LOGGER.setLevel(logging.DEBUG)
    #manual = MethodCall("selve.GW.iveo.getIDs",[])
    portname = '/dev/virtual-tty'
    gat = Gateway(portname, False)


    gat.discover()
    #devices = list(gat.devices.values())
    #device = IveoDevice(gat, 0)
    #device.stop(False)
    #gat.list_devices()

    # device1 = IveoDevice(gat, 1)
    # device2 = IveoDevice(gat, 2)
    # device1.moveDown()
    # time.sleep(5)
    # device1.moveUp()
    # device2.moveDown()
    # time.sleep(3)
    # device1.stop()
    # device2.stop
    # time.sleep(1)
    # device1.stop()
    #command = IveoCommandGetIds()
    #command.execute(gat)
    #print (command.ids)
    #response = b'<?xml version="1.0"? encoding="UTF-8">\r\n<methodResponse>\r\n\t<array>\r\n\t\t<string>selve.GW.iveo.commandManual</string>\r\n\t\t<int>1</int>\r\n\t</array>\r\n</methodResponse>\r\n\n<?xml version="1.0"? encoding="UTF-8">\r\n<methodCall>\r\n<methodName>selve.GW.iveo.commandResult</methodName>\r\n\t<array>\r\n\t\t<int>0</int>\r\n\t\t<base64>AQAAAAAAAAA=</base64>\r\n\t\t<int>0</int>\r\n\t</array>\r\n</methodCall>\r\n\n'
    #c = response.decode()
    #print(c)
    #deserialize(response)

