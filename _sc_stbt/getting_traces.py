

# -*- coding: utf-8 -*-
"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""


from pyspawn import *
import stbt
import sc_stbt
import time



def active_trace_telnet( ip_address=None, set_cc_level=None):
    if ip_address is None:
        ip_address = stbt.get_config("Traces", "trace_ip_address")
    if set_cc_level is None:
        set_cc_level = stbt.get_config("Traces", "set_cc_level")
        set_cc_level=set_cc_level.split(',')

    filenamelog = "traces_history.txt"
    fichier = open(filenamelog, "a+")
    cmd = Spawn("telnet " + ip_address)
    cmd.launch(log_input=fichier)
    cmd.expect('/ #', timeout=10)
    sc_stbt.debug("connected to telnet")
    cmd.sendline("ccsh")
    cmd.expect('ccsh #',timeout=10)
    cmd.sendline("select_output syslog")
    cmd.expect('select output syslog ok',timeout=10)
    cmd.sendline("bye")
    cmd.expect(' #',timeout=10)
    cmd.sendline("ccsh")
    cmd.expect('ccsh #',timeout=10)
    for i in range(len(set_cc_level)):
        cmd.sendline("set_cc_level " +set_cc_level[i])
        cmd.expect('ccsh #' , timeout=20)
        x = cmd.get_output()
        if   x.find('ok') > 0 :
             sc_stbt.debug('Traces activated')
        else:
             assert False , 'Blocked : stbt can not activate traces'
    cmd.sendline("bye")
    cmd.expect(' #',timeout=10)
    cmd.sendline("exit")
    cmd.expect('',timeout=10)



def get_traces_telnet(ip_address=None, time_out_traces=None):

    if ip_address is None:
        ip_address = stbt.get_config("Traces", "trace_ip_address")
    if time_out_traces is None:
        time_out_traces= eval(stbt.get_config("Traces", "time_out_traces"))

    filenamelog = "traces_history.txt"
    fichier = open(filenamelog, "w")
    cmd = Spawn("telnet " + ip_address)
    cmd.launch(log_input=fichier)
    cmd.expect('/ #', timeout=10)
    sc_stbt.debug('waiting for traces')
    cmd.sendline("cat /tmp/syslog.log")
    start = time.time()
    cmd.expect("/ #" , timeout=time_out_traces )
    stop= time.time()
    Trace= cmd.get_output()
    Traces = open("traces.log", "a")
    Traces.write(Trace)
    Traces.close()
    if stop - start  < time_out_traces :
        return sc_stbt.debug('Traces successfully getted')
    else:
        assert False ,"time out traces expired"

def active_traces_minicom(trace_device=None , set_cc_level=None):
    if trace_device is None:
        trace_device= stbt.get_config("Traces", "trace_device")
    if set_cc_level is None:
        set_cc_level = stbt.get_config("Traces", "set_cc_level")
        set_cc_level=set_cc_level.split(',')

    filenamelog = "traces_his.txt"
    fichier = open(filenamelog, "a")
    cmd = Spawn("minicom -w -D "+trace_device)
    cmd.launch(log_input=fichier)
    cmd.expect('Press CTRL-A Z for help on special keys', timeout=10)
    sc_stbt.debug("connected to minicom")
    cmd.sendcontrol('c')
    cmd.expect('#', timeout=100)
    cmd.sendline("ccsh")
    cmd.expect('ccsh #', timeout=10)
    stbt.debug("connected to ccsh 1")
    cmd.sendline("select_output syslog")
    stbt.debug("cosmocat modified : output syslog")
    cmd.expect('ccsh #',timeout=10 )
    cmd.sendline("bye")
    cmd.expect('#', timeout=10)
    cmd.sendline("ccsh")
    cmd.expect('ccsh #', timeout=10)

    for i in range(len(set_cc_level)):
        cmd.sendline("set_cc_level " +set_cc_level[i])
        cmd.expect('ccsh #' , timeout=20)
        x = cmd.get_output()
        if   x.find('ok') > 0 :
             sc_stbt.debug('Traces activated')
        else:
             assert False , 'Blocked : stbt can not activate traces'
    cmd.sendline("bye")
    cmd.expect('#', timeout=10)




def get_traces_minicom(trace_device=None, time_out_traces=None):
    if trace_device is None:
        trace_device= stbt.get_config("Traces", "trace_device")
    if time_out_traces is None:
        time_out_traces= eval(stbt.get_config("Traces", "time_out_traces"))
    filenamelog = "traces_his.txt"
    fichier = open(filenamelog, "a")
    cmd = Spawn("minicom -w -D "+trace_device)
    cmd.launch(log_input=fichier)
    cmd.sendline("cat /tmp/syslog.log")
    sc_stbt.debug('waiting for traces')
    start = time.time()
    cmd.expect("#   ",timeout=time_out_traces)
    stop = time.time()
    Trace= cmd.get_output()
    Traces = open("traces.log", "a")
    Traces.write(Trace)
    if stop - start < time_out_traces :
        return sc_stbt.debug('Traces successfully getted')
    else:
        assert False ,"time out traces expired"



def active_traces(type_connection=None):
    if type_connection is None:
        type_connection= stbt.get_config("Traces", "type_connection")
    if type_connection == "telnet":
        active_trace_telnet()
    elif type_connection == "minicom":
        active_traces_minicom()
    # else:
    #     assert False , sc_stbt.debug("NO type_connection defined")

def get_traces(type_connection=None):
    if type_connection is None:
        type_connection= stbt.get_config("Traces", "type_connection")
    if type_connection == "telnet":
        get_traces_telnet()
    elif type_connection == "minicom":
        get_traces_minicom()
    # else:
    #     assert False , sc_stbt.debug("NO type_connection defined")


def get_date(type_connection=None, trace_device=None , ip_address=None):

    if trace_device is None:
        trace_device= stbt.get_config("Traces", "trace_device")
    if ip_address is None:
        ip_address = stbt.get_config("Traces", "trace_ip_address")
    if type_connection is None:
        type_connection= stbt.get_config("Traces", "type_connection")

    filenamelog = "traces_his.txt"
    fichier = open(filenamelog, "a")

    if type_connection=='minicom':
        cmd = Spawn("minicom -w -D "+trace_device)
        cmd.launch(log_input=fichier)
        cmd.expect('Press CTRL-A Z for help on special keys', timeout=10)
        sc_stbt.debug("connected to minicom")
        cmd.sendcontrol('c')
        cmd.expect('login',timeout=5)
        if cmd.get_out()=='login':
            cmd.sendline('root')
        cmd.expect('#', timeout=10)
        cmd.sendline("date | cut -d ' ' -f 4")
        cmd.expect('(\d\d):(\d\d):(\d\d)', timeout=10)
        date=cmd.get_out()
        print "date" , date
        return date
    elif  type_connection=='telnet':
        cmd = Spawn("telnet " + ip_address)
        cmd.launch(log_input=fichier)
        cmd.expect('/ #', timeout=10)
        cmd.sendline("date | cut -d ' ' -f 4")
        cmd.expect('(\d\d):(\d\d):(\d\d)', timeout=10)
        date=cmd.get_out()
        print "date" , date
        return date
    else :
        assert False , "Type of connection not selected"

