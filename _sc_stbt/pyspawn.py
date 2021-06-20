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
import os
import pexpect
import sys
import functools
import struct, fcntl, termios, signal
EOF = pexpect.EOF


class Spawn():
    def __init__(self, command, sudo=False, Password=None):
        self.child = None
        self.spawn_command = None
        self.sudo = sudo
        self.password = Password

        if self.sudo == True:
            self.spawn_command = 'sudo -k -p "password:" ' + command
        else:
            self.spawn_command = command


    def expect(self, line, timeout=None):
        try:
            index = self.child.expect([line,  ], timeout)
            if index == 0:
                return index
            elif index == 1:
                # print "Problem expecting your entry. Got another entry."
                return index
        except pexpect.EOF:
            # print "Problem expecting your entry. Got EOF"
            return None
        except pexpect.TIMEOUT:
            # print "Problem expecting your entry. Got TIMEOUT"
            return None


    def readlines(self, sizehint):

        try:
            ch= self.child.readlines(sizehint=sizehint)
            return ch
        except pexpect.EOF:
            # print "Problem expecting your entry. Got EOF"
            return ch
        except pexpect.TIMEOUT:
            # print "Problem expecting your entry. Got TIMEOUT"
            return ch





    def launch(self, log_input=None, log_output=None):
        self.child = pexpect.spawn(self.spawn_command)

        if self.sudo:
            try:
                opt = self.child.expect('password:')
                self.child.sendline(self.password)
            except:
                pass

        if log_input == None:
            log_input = sys.stdin

        if log_output == None:
            log_output = sys.stdout

        self.child.logfile_read = log_input
        self.child.logfile_send = log_output


    def sendline(self, line):
        try:
            self.child.sendline(line)
        except:
            return -1

    def sendcontrol(self, control):
        try:
            self.child.sendcontrol(control)
        except:
            return -1

    def get_output(self, force_log=False):
        if force_log == True:
            self.expect(EOF, 0.5)  # This line for flushing logfile
        return self.child.before

    def get_out(self, force_log=False):
        if force_log == True:
            self.expect(EOF, 0.5)  # This line for flushing logfile
        return self.child.after


    def get_exitstatus(self):
        return self.child.exitstatus

    def get_signalstatus(self):
        return self.child.signalstatus

    def get_status(self):
        return self.child.status

    def kill(self):
        self.child.kill(9)
        # print "Killed process. Exit status"
        # print self.get_exitstatus()
        # print self.get_signalstatus()
        # print self.get_status()

    def terminate(self):
        if self.child != None:
            try:
                self.expect(EOF, 0.5)  # This line for flushing logfile
            except:
                self.child.close()
                # print "Error during Spawn() destruction"
                return (self.get_exitstatus(), self.get_signalstatus(), self.get_status())
            else:
                self.child.close()
                # print "Terminated process. Exit status"
                return (self.get_exitstatus(), self.get_signalstatus(), self.get_status())

    def __del__(self):
        if self.child != None:
            try:
                self.expect(EOF, 0.5)  # This line for flushing logfile
            except:
                self.child.close()
                # print "Error during Spawn() destruction"
                # print self.get_exitstatus()
                # print self.get_signalstatus()
                # print self.get_status()
            else:
                self.child.close()
                # print "Terminated process. Exit status"
                # print self.get_exitstatus()
                # print self.get_signalstatus()
                # print self.get_status()

