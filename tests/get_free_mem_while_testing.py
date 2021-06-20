"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""
import sc_stbt
import time
import os
import stbt
from _sc_stbt.pyspawn import *

video = sc_stbt.video_tests()
trace_device= stbt.get_config("Traces", "trace_device")

cmd = Spawn("minicom -w -D"+trace_device)

def initialize():
    """
    initialize : connect to minicom
    :return:
    """
    filenamelog = "traces_his.txt"
    fichier = open(filenamelog, "a")
    cmd.launch(log_input=fichier)
    cmd.expect('Press CTRL-A Z for help on special keys', timeout=10)
    sc_stbt.debug("connected to minicom")
    cmd.sendcontrol('c')
    cmd.expect('#', timeout=100)

def get_free_memory(timeout):
    """

    :param timeout:
    :return:
    """
    start_time = time.time()
    j = 2
    initialize()
    while time.time() - start_time < timeout:
        cmd.sendline("cat /proc/meminfo | grep 'MemFree:\|MemTotal:'")
        cmd.expect('cat /proc/meminfo #', timeout=10)
        stbt.debug("cat done")
        free_mem = (os.popen("grep 'MemFree' traces_his.txt | awk '{if(NR=="+str(j)+") print $0 }'").readlines())
        total_mem = (os.popen("grep 'MemTotal' traces_his.txt | awk '{if(NR=="+str(j)+") print $0 }'").readlines())
        print free_mem[0].split(":")[1]
        print total_mem[0].split(":")[1]
        stbt.draw_text("Mem Free : " +(free_mem[0].split(":")[1]).strip()+ " / " +(total_mem[0].split(":")[1]).strip())
        j = j + 2
        sc_stbt.wait(3)
    os.popen("rm -rf traces_his.txt")
    cmd.terminate()


sc_stbt.repeat(lambda : sc_stbt.multi_threading(callable_1 = lambda :video.motion(polling_secs=60),
                                                callable_2 = lambda :get_free_memory(timeout = 60)),occurence = 3)