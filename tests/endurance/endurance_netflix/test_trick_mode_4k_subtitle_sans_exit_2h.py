import sc_stbt
from android import goto_netflix




def trick_mode_subtitle():

    # goto_netflix()
    sc_stbt.open_video_netflix(movie_name="cargo")
    sc_stbt.active_subtitles_netflix()
    sc_stbt.repeat(lambda: sc_stbt.forward_play_netflix(), occurence=3, time_out=3600 )
    sc_stbt.repeat(lambda: sc_stbt.rewind_play_netflix(), occurence=3,time_out=3600 )
    sc_stbt.back_to_netflix_movie_menu()
    # sc_stbt.test_exit_netflix()

#################################API Call#################################################


sc_stbt.repeat(lambda: trick_mode_subtitle(),
               occurence=15,
               wait_=4 )