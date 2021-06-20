#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""
import socket
from _stbt.config import get_config

class Irtrans(object):
    """Irtrans class"""
    control = get_config('global', 'control')
    command = control.split(':')[2]
    HOST = 'localhost'  # Symbolic name meaning the local host
    PORT = 21000  # Arbitrary non-privileged port
    _debug_level = 0
    _socket = None
    "constructor of IRTRANS " \
    "Inputs are :" \
    "the local server" \
    "port of communication between client and server" \
    "command name"
    def __init__(self, hostname=HOST, port=PORT, remote=command):
        self.hostname = hostname
        self.port = port
        self.remote = remote
    def connect_irtrans(self):
        """Create the socket between SERVER(irserver) and CLIENT(irclient)"""
        global _socket
        try:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.connect((self.HOST, self.PORT))
            return _socket

        except socket.error, ex:
            pass
    def get_socket(self):
        """return socket"""
        return _socket
    def send_command(self):
        """Connection verification between Server and client"""
        # Workaround : send to server en empty 'Asnd'
        data = "Asnd \n"
        _socket.send(data)
        data = _socket.recv(100)
        if data == "**00023 RESULT_SEND OK":
            return True
        else:
            return False
    def disconnect_irtrans(self):
        """Close socket"""
        try:
            _socket.close()
        except socket.error, ex:
            print "Error discconnecting to host \n %s" % ex
    def receive_IR_code(self):
        """Learnig remote Buttons to irtrans"""
        data = _socket.recv(100)
        print "Received Data : %s" % data
        if "RCV_COM" in data:
            remote = data[data.find("RCV_COM") + 7:data.find(",")]
            substring = data[data.find(remote) + len(remote) + 1:]
            remote.lower()
            # print "Remote Name : " + remote
            command = substring[:substring.find(",")]
            # print "Command Name : " + command
            return remote, command
        else:
            return "", ""
    def power_switch(status_power):
        """Input : True /False" \
         "the aim of this function is to power on/off the irserver"""
        if status_power:
            data = "Apower ON\n"
            _socket.send(data)
        else:
            data = "Apower OFF\n"
            _socket.send(data)
    def send_IR_code(self, remote, command):
        """input : remote name and the command name" \
        "output : Sending key"""
        self.connect_irtrans()
        data = "Asnd %s,%s\n" % (remote, command)
        _socket.send(data)
        data = _socket.recv(100)
        if data == "**00023 RESULT_SEND OK":
            return True
        else:
            return False
    def check_connexion(self):
        """Cheking communication between irserver and irclient"""
        try:
            self.connect_irtrans()
            _socket.send("Check Connection !!")
            return True
        except:
            return False
    def press(self, key):
        """Send the selected key to STB"""
        self.send_IR_code(self.remote, key)
