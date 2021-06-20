import sc_stbt


def open_exit_netflix():
    """

    :return:
    """
    sc_stbt.go_to_netflix()
    sc_stbt.wait(20)
    sc_stbt.test_exit_netflix()



#################################API Call#################################################



sc_stbt.repeat(lambda: open_exit_netflix(), occurence=35, time_out=150, wait_=60 )