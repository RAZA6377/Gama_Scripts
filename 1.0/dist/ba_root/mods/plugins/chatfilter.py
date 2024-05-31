import babase as ba
import _babase as _ba
import bascenev1 as bs
import bascenev1lib as bsl
import bauiv1 as bui
import datafiles.votingmachine as vh
from datetime import datetime


def filter_chat_message(msg, client_id):
    now = datetime.now()
    if client_id == -1:
        if msg.startswith("/"):
            print(msg)
            return None
        return msg
    acid = ""
    displaystring = ""
    currentname = ""

    for i in bs.get_game_roster():
        if i['client_id'] == client_id:
            acid = i['account_id']
            try:
                currentname = i['players'][0]['name_full']
            except:
                currentname = "<in-lobby>"
            displaystring = i['display_string']
    
    if msg in ["end", "dv", "nv", "sm"]:
        print("worked")
        vh.vote(acid, client_id, msg)
    if "bsdk" in msg:
        print("Gali Printed")
    else:
        print("Nothing Happend")
