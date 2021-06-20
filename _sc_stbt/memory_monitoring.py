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
import csv
import pandas as pd
import os


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



def get_logs(filenamelog=None, ip_address=None ,command=None ):
    """
    get_logs: copy in the filenamelog MemAvailable and MemFree
    :param filenamelog: the file name
    :param ip_address: ip address of
    :param command: command of PID

    """
    if filenamelog is None:
        filenamelog = "pid.txt"
    if ip_address is None:
        ip_address = stbt.get_config("memory_monitoring", "ip_address")

    date = time.ctime(time.time())
    fichier = open(filenamelog, "a")

    cmd = Spawn("telnet " + ip_address)
    cmd.launch(log_input=fichier)
    cmd.expect('/ #', timeout=10)

    if command is None:

     command= stbt.get_config("memory_monitoring", "command_list")
     command=command.split(',')

    for i in range(len(command)):

        cmd.sendline("ps | grep "+command[i]+ "| cut -f 2 -d ' '")
        cmd.expect('/ #', timeout=10)
        PID=cmd.get_output().split('\n')
        command_=command[i]

        for i in range(len(PID[:-3])) :

            PID2=str([int(s) for s in PID[i+1].split() if s.isdigit()])
            cmd.sendline("cat /proc/"+PID2[1:-1]+"/status | grep VmRSS  | cut -d ':' -f 2")
            cmd.expect('/ #', timeout=10)
            VmRSS=cmd.get_output().split('  ')
            VmRSS=str([int(s) for s in VmRSS[-1].split() if s.isdigit()])
            VmRSS=str(VmRSS[1:-1])

            file = open('VmRSS.csv', 'a')

            if int(VmRSS) != 2 :
                data=[date,int(VmRSS),PID2[1:-1]+command_]
                writer = csv.writer(file)
                writer.writerow(data)

            file.close()

    fichier.close()

def arrange_file_mem():

        """
   arrange_file_mem : modify_and_arrange_the_csv_file

    """

        file= open("VmRSs_test.csv", "w+")
        data = csv.reader(open('VmRSS.csv'))
        writer=csv.DictWriter(file, fieldnames=["Date", "VmRSS","PID"])
        writer.writeheader()
        fileWriter = csv.writer(file)
        for row in data:
            fileWriter.writerow(row)
        file.close()

def plot_mem(file="VmRSs_test.csv",figure="memory_monitoring.png"):

        """
    plot_mem: plot_data_getted_from_the_csv_file
    :param file=input_file
    :param figure=title_of_the_output

    """
        arrange_file_mem()
        df = pd.read_csv(file )
        df.head()
        pid=df.pivot_table(values=['VmRSS'],rows=['Date'],cols=['PID'])
        pid.head()
        fig = pid.plot(kind='line', use_index=True ,figsize=(15,10) , title='memory_monitoring'  , rot=15, fontsize='small', grid= True , label=True)
        fig.set_ylabel("VmRSS (MB)",fontsize=12 )
        fig.yaxis.set_ticklabels(range(0,200,20))
        fig.set_xlabel('Date' , animated = False  ,rasterized= False )
        fig.xaxis.set_tick_params(labelsize ="small")
        fig.legend(loc='best' ,ncol=2, fancybox=False , shadow=False , frameon=False ,fontsize='medium' )
        fig = fig.get_figure()
        fig.savefig(figure)
        pid.to_csv("memory_monitoring.csv")
        os.remove('VmRSs_test.csv')
        os.remove('VmRSS.csv')

def start_monitoring(callable, interval_secs=None):

    """
    start the memory monitoring with calling  thread_monitoring
    :param callable: function to get logs
    :param interval_secs: Seconds interval timer to call thread
    """
    if interval_secs is None:
        interval_secs = stbt.get_config("memory_monitoring", "interval_secs", type_=int)

    # Creation of thread to monitor memory
    thread_memory_monitoring = monitoring(callable, interval_secs)
    # Start the execution
    thread_memory_monitoring.start()





