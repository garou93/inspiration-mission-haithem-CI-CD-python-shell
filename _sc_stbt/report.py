__author__ = 'haithem'

import requests
import sys
import stbt


mode = sys.argv[1]
if mode == '1' :
    version = str(sys.argv[2])
    if '_' in version :
        version= version.split('_')[0]+'_'+version.split('_')[-1]
    product = stbt.get_config("report" , "product_r" )
    config = stbt.get_config("report" , "config_r"  )
    board= stbt.get_config("report" , "board_r" , type_=int)
    week = stbt.get_config("report" , "week_r" , type_=int)
    day = stbt.get_config("report" ,'day_r' , type_= int)
    state = int(sys.argv[3])

    ip_server = stbt.get_config("report" , "ip_server_r" )


    r = requests.post("http://"+ip_server+"/Layout", data={'product': product, 'config': config , 'board': board , 'week' : week , 'day' : day , \
                                                                "version" : version , "state" : state })
    print(r.status_code, r.reason)

elif mode == '2' :

    print sys.argv[2]
    print sys.argv[3]

    idTest = sys.argv[2]
    state = sys.argv[3]
    r = requests.post("http://127.0.0.1:8080/VALID", data={'idTest': idTest, 'state': state } )
    print(r.status_code, r.reason)
