Python control of selve devices through USB-RF Gateway
======================================================

|PyPI version|

A simple Python API for controlling RF Blinds / shutters / awning from selve using a USB-RF Gateway.

For the HTTP server, check out https://github.com/gillesmaes/python-selve-usbrf-server. 

The complete protocol specification can be found at `selve <https://www.selve.de/de/service/software-updates/service-entwicklungstool-commeo-usb-rf-gateway/>`_

Example of use
--------------

Create a new instance of the gateway:

.. code-block:: python

    gat = Gateway(hostname)


hostname is the address of the remote HTTP server that's hooked up to the USB serial interface.

By default the gateway will discover all Iveo devices already registered onto the gateway.

To access them:

.. code-block:: python

    gat.devices()

Will return a list of IveoDevices()

Each IveoDevice can be controlled by using the already defined commands: stop() moveUp() moveToIntermediatePosition1() and moveToIntermediatePosition2()

The library also allows to send directly commands to the gateway without the need of using the IveoDevice abstraction just create the command and execute using the gateway:

.. code-block:: python

    command = IveoCommandGetIds()
    command.execute(gat)

Once executed the response is stored in the command instance for later user or just to discard.

.. |PyPI version| image:: https://badge.fury.io/py/python-selve-http.svg
   :target: https://badge.fury.io/py/python-selve-http






