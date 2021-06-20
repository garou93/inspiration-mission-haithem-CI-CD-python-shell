import sc_stbt
from android import goto_netflix


def check_subtitle():

    sc_stbt.go_to_netflix()
    sc_stbt.open_video_netflix()
    sc_stbt.active_subtitles_netflix()
    sc_stbt.back_to_netflix_movie_menu()
    # sc_stbt.test_exit_netflix()

#################################API Call#################################################

check_subtitle()