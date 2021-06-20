import sc_stbt





def test1():

    sc_stbt.go_to_youtube()
    sc_stbt.test_open_video_youtube(video_name="4k")
    sc_stbt.test_youtube_motion(test_secs=120,
                        polling_secs=40,
                        interval_secs=5)
    sc_stbt.test_youtube_pause()
    sc_stbt.wait(20)
    sc_stbt.test_youtube_play()
    sc_stbt.wait(20)
    sc_stbt.test_youtube_fastforward()
    sc_stbt.test_youtube_rewind()

#################################API Call#################################################

sc_stbt.repeat(lambda: test1(),
               occurence=15)
