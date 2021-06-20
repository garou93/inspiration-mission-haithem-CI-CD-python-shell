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
import threading
import stbt
from pyspawn import *
import sc_stbt


class monitoring(threading.Thread):
    def __init__(self, callable, interval_secs):
        """
        Constructor
        :param callable: function to get logs
        :param interval_secs:Seconds interval timer to call thread
        """
        threading.Thread.__init__(self)
        # Daemonize thread: allow the main test to exit even the thread_monitoring is running
        self.setDaemon(True)
        self.callable = callable
        self.interval_secs = interval_secs

    def run(self):
        """
        The run() method will be started and it will run in the background
        until the test exits.
        """
        while True:
            try:
                self.callable()
            except:
                print"[ERROR] ERROR DETECTED IN GET_LOG "
                pass
            print "---------calling thread after interval_secs ---------"
            time.sleep(self.interval_secs)


def get_logs(filenamelog=None, ip_address=None):
    """
    get_logs: copy in the filenamelog MemAvailable and MemFree
    :param filenamelog: the file name
    :param ip_address: ip address of stb
    """

    if filenamelog is None:
        filenamelog = "logs.txt"
    if ip_address is None:
        ip_address = stbt.get_config("memory_monitoring", "ip_address")
    date = time.ctime(time.time())
    fichier = open(filenamelog, "a")
    cmd = Spawn("telnet " + ip_address)
    cmd.launch(log_input=fichier)
    cmd.expect('/ #', timeout=10)
    cmd.sendline('echo "----MEMORY USED BY ALL PROCESSES IN %s ----" > /dev/ttyS0' % (date))
    cmd.expect('/ #', timeout=10)
    cmd.sendline('cat /proc/meminfo |grep -i MemAvailable')
    cmd.expect('/ #', timeout=10)
    cmd.sendline('cat /proc/meminfo |grep -i MemFree')
    # cmd.sendline('free')
    cmd.expect('/ #', timeout=10)
    # cmd.sendline('echo "---- MEMORY USED BY MIDDLEWARE IN %s ----" > /dev/ttyS0' % (date))
    # cmd.expect('/ #', timeout=10)
    # cmd.sendline('cat /proc/1144/status |grep -i VmSize')
    # cmd.expect('/ #', timeout=10)
    fichier.close()

def start_monitoring(callable, interval_secs=None):

    """
    start the memory monitoring with calling  thread_monitoring
    :param callable: function to get logs
    :param interval_secs: Seconds interval timer to call thread
    """
    if interval_secs is None:
        interval_secs = stbt.get_config("memory_monitoring", "interval_secs", type_=int)

    sc_stbt.debug("===STARTING THREAD MONITORING===")
    # Creation of thread to monitor memory
    thread_memory_monitoring = monitoring(callable, interval_secs)
    # Start the execution
    thread_memory_monitoring.start()


