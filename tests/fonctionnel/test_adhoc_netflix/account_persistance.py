import sc_stbt
from android import goto_netflix



def persistance():

    sc_stbt.test_power_on(lambda: sc_stbt.is_wakeup())
    sc_stbt.wait(60)
    sc_stbt.combo_press(combo=["KEY_HOME"],number_press=5)
    sc_stbt.wait(5)
    sc_stbt.go_to_netflix()
    sc_stbt.open_video_netflix()

#################################API Call#################################################

persistance()