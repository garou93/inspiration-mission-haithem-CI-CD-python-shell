
import sc_stbt
from android import goto_netflix

def title_search():

    sc_stbt.go_to_netflix()
    sc_stbt.open_video_netflix(movie_name="house of cards")


#################################API Call#################################################

title_search()