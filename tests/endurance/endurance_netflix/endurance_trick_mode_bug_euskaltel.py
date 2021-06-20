
import sc_stbt
from android import goto_netflix



#################################API Call#################################################

sc_stbt.go_to_netflix()
sc_stbt.open_video_netflix()
sc_stbt.repeat(lambda: sc_stbt.forward_play_netflix(), occurence=4)
sc_stbt.repeat(lambda: sc_stbt.rewind_play_netflix(), occurence=4)
sc_stbt.back_to_netflix_movie_menu()
# sc_stbt.test_exit_netflix()
