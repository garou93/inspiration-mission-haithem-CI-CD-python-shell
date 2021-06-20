import sc_stbt



def navigation_menu():

     sc_stbt.go_to_youtube()
     sc_stbt.test_navigation_youtube(navigation_occurence=2)
     sc_stbt.test_navigation_youtube(navigation_press="KEY_DOWN", navigation_occurence=5)
     sc_stbt.test_navigation_youtube(navigation_press="KEY_UP", navigation_occurence=3)


#################################API Call#################################################



sc_stbt.repeat(lambda: navigation_menu(),
               occurence=150)

