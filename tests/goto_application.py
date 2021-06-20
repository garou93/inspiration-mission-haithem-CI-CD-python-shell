"""
	Title:			
	Description:
	Author:			haithem ben abdelaziz
	Date:			
	Version: 		
	Environment:
"""


import stbt


mdw =  eval(stbt.get_config("android", "android"))

def go_to_netflix():
    """
    go_to_netflix: goto netflix application
    :return:
    """
    if mdw:
        from android import goto_netflix
        goto_netflix()
    else:
        import alticeus
        alticeus.goto_netflix()

def go_to_youtube():
    """
    go_to_youtube: goto youtube application
    :return:
    """
    if mdw:
        from android import goto_youtube
        goto_youtube()
    else:
        import alticeus
        alticeus.goto_youtube()

def go_to_amazon():
    """
    go_to_amazon: goto amazon application
    :return:
    """
    if mdw:
        from android import goto_amazon
        goto_amazon()
    else:
        import alticeus
        alticeus.goto_amazon()