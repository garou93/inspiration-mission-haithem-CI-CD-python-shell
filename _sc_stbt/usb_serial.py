#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""

import time
import logging
import serial
import stbt


DEV_POWER = '/dev/powerswitch'
DEV_HDMI = '/dev/hdmiswitch'
ON = 'N'
OFF = 'F'
ALL_OFF = 'F1F2F3F4'

power_outlet = stbt.get_config("power", "outlet")
power_device = stbt.get_config("power", "device")
power_port = stbt.get_config("power", "port", type_=int)

hdmi_port = stbt.get_config("hdmi_switcher", "port", type_=int)

hdmi_device = stbt.get_config("hdmi_switcher", "device")

class USBserial:
    """ Class to control serial port
        pySerial opens port in constructor,
        and I was calling "open" method after constructor
    """

    def __init__(self, mount, baudrate=115200, timeout=5):
        self.port = serial.Serial(port=mount, baudrate=baudrate,
                                  timeout=timeout, writeTimeout=timeout)
        try:
            self.port.open()
        except serial.SerialException:
            logging.error('Got exception open is done on constructor')
            # newer version of pySerial opens port in constructor,
            # and calling "open" method after constructor lead to exception
            # WA: close and open it to keep backward compatibility
            self.port.close()
            self.port.baudrate = baudrate
            self.port.bytesize = serial.EIGHTBITS
            self.port.parity = serial.PARITY_NONE
            self.port.stopbits = serial.STOPBITS_TWO
            #self.port.stopbits = stopbits
            self.port.xonxoff = False
            self.port.rtscts = False
            self.port.dsrdtr = False
            self.port.open()
        time.sleep(2)

    def open(self):
        ''' Open the serial port.'''
        self.port.open()

    def close(self):
        ''' Purge buffers and Close the serial port.'''
        self.port.flushInput()
        time.sleep(2)
        self.port.flushOutput()
        time.sleep(2)
        self.port.close()

    def send(self, msg):
        """ Send msg """
        self.port.write(msg)
        send_time = time.time()
        time.sleep(2)
        self.recv()
        return send_time

    def recv(self):
        """ Read """
        msg = self.port.read(self.port.inWaiting())
        logging.info("Read Rx:\n%s", msg)
        return msg


def set_hdmi_input(port=None):
    if port is None:
        port = stbt.get_config("hdmi_switcher", "port", type_=int)
    hdmiswitch_version = stbt.get_config("hdmi_switcher", "hdmiswitch_version")

    """ Enable the hdmi port requested for test"""
    ser_hdmi = USBserial(mount=hdmi_device, baudrate=19200)
    ser_hdmi.send('pod off\r\n')

    if hdmiswitch_version == 'vs481a':
        ser_hdmi.send('sw o01 i0' + str(port) + '\r\n')
        time.sleep(0.05)
        ser_hdmi.send('sw o01 i0' + str(port) + '\r\n')
    elif hdmiswitch_version == 'vs481b':
        ser_hdmi.send('sw i0' + str(port) + '\r\n')
        time.sleep(0.05)
        ser_hdmi.send('sw i0' + str(port) + '\r\n')
    #stbt.draw_text("Setting HDMI input number" + str(port))
    logging.info("HDMI : %d", str(port))
    # ser_hdmi.close()


def set_power(port1=OFF, port2=OFF, port3=OFF, port4=OFF):
    """ Set the requested power switch port """
    ser_power = USBserial(mount=DEV_POWER)
    cmd = port1 + '1' + port2 + '2' + port3 + '3' + port4 + '4'
    ser_power.send(str(cmd))
    logging.info("Command Power: %s", str(cmd))
    # ser_power.close()


def power_off(text=ALL_OFF, port=1, state=OFF):
    """ Set the command for power switch in OFF state"""
    if power_outlet == "epower4":
        cmd = 'P' + str(port) + '=0\r'
    elif power_outlet == "epower4v2":
        cmd = '/P0' + str(port) + '=0\r'
    else:
        if port == '0':
            cmd=text
        else:
            port = (port - 1) * 2
            cmd = text[:port] + state + text[port + 1:]
    return str(cmd)


def power_on(text=ALL_OFF, port=1, state=ON):
    """ Set the command for power switch in On state"""

    if power_outlet == "epower4":
        cmd = 'P' + str(port) + '=1\r'
    elif power_outlet == "epower4v2":
        cmd = '/P0' + str(port) + '=1\r'
    else:
        port = (port - 1) * 2
        cmd = text[:port] + state + text[port + 1:]
    return str(cmd)


def power_init():
    logging.info("Init %s", power_outlet)
    if "epower4" in power_outlet:
        _pwr = USBserial(mount=power_device, baudrate=9600)
    else:
        _pwr = USBserial(mount=DEV_POWER)
    logging.info("Init %s", power_outlet)
    # cmd = power_off(port=0)
    # _pwr.send(cmd)
    # time.sleep(3)
    return _pwr


def set_power_off(port=None):
    """ Disable the requested port """
    
    pwr = power_init()
    if port is None:
        port = power_port
    cmd = power_off(port=port)
    logging.info("Power OFF Port(%d) -> %s", int(port), cmd)
    pwr.send(cmd)
    pwr.close()

def set_power_on(port=None):
    """ Enable the requested port """
    
    pwr = power_init()
    if port is None:
        port = power_port
    cmd = power_on(port=port)
    logging.info("Power ON  Port(%d) -> %s", int(port), cmd)
    pwr.send(cmd)
    pwr.close()

def epower(cmd=None):
    """

    :param cmd: N for on F for off (cmd=N1F2F3N4
            on port 1 4 off 2 3
    :return:
    """
    if cmd==None:
        cmd="N1N2N3N4"

    pwr=power_init()
    pwr.send(cmd)


