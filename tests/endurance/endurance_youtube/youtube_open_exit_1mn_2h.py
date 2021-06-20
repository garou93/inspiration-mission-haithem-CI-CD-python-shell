import sc_stbt




def open_youtube():
    sc_stbt.go_to_youtube()
    sc_stbt.combo_press(combo=["KEY_HOME"],number_press=3)
    sc_stbt.wait(60)
#################################API Call#################################################

sc_stbt.repeat(lambda: open_youtube(),
               occurence=580,
               wait_=4 )