import sc_stbt




def test():
    print"-----------------Hello--------------------"
    sc_stbt.press("KEY_RIGHT")
    sc_stbt.wait(20)
    sc_stbt.debug("=========Hiiii After Press=============")

sc_stbt.start_monitoring(lambda : sc_stbt.get_logs())
test()
