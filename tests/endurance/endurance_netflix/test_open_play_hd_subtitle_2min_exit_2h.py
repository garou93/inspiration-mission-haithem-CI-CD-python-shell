import sc_stbt
from android import goto_netflix



def netflix_hd_subtitle():

    goto_netflix()
    sc_stbt.open_video_netflix(movie_name="cars")
    sc_stbt.active_subtitles_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    sc_stbt.combo_press(combo=["KEY_HOME"],number_press=3)
    sc_stbt.wait(60)
    # sc_stbt.test_exit_netflix()


#################################API Call#################################################

sc_stbt.repeat(lambda: netflix_hd_subtitle(),
               occurence=20,
                wait_=4 )