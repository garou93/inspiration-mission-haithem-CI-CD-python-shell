import sc_stbt
from android import goto_netflix




def open_exit_netflix():

    sc_stbt.go_to_netflix()
    sc_stbt.wait(3)
    sc_stbt.combo_press(combo=["KEY_HOME"],number_press=3)



#################################API Call#################################################



sc_stbt.repeat(lambda: open_exit_netflix(), occurence=7200, time_out=160, wait_=60 )