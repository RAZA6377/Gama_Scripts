import babase as ba 
import bascenev1 as bs 
from bascenev1 import chatmessage as cmsg, broadcastmessage as bmsg
import time

players = []
session = bs.get_foreground_host_session
afk_cd = 20
check_interval = 1  # Check every second

def get_player_info(clientID: int):
    clientID = int(clientID)
    info = {}
    for i in _ba.get_game_roster():
        if i['client_id'] == clientID:
            info['ds'] = i['display_string']
            info['aid'] = i['account_id']
            info['p'] = i['players']
            break
    return info
        
def add(clientid: int):
    if clientid not in players:
        players.append(clientid)
        
def remove(clientid: int):
    if clientid in players:
        players.remove(clientid)
        
def check_afk():
    global players
    global afk_cd
    global session

    host_session = session()
    if host_session is None:
        print("No active host session.")
        return

    print("Checking for AFK players...")

    for player in host_session.sessionplayers:
        last_input = int(player.inputdevice._last_input_time)
        print(f"Last input for player {player} (client ID {player.inputdevice.client_id}): {last_input}")
        cid = player.inputdevice.client_id
        now = int(time.time())
        if now in range(last_input, last_input + afk_cd):
            remain_time = afk_cd - (now - last_input)
            bmsg(f"Press Any Button Within {remain_time} Seconds", color=(1, 0, 0), transient=True, clients=[cid])
        if now > last_input + afk_cd:
            print(f"Removing player {player} (client ID {cid}) for being AFK.")
            player.remove_from_game()
            add(cid)
            
    try:
        for clientid in players:
            info = get_player_info(clientid)
            cmsg(f"{info['ds']} Removed From Game | AFK")
            players.remove(clientid)
    except Exception as e:
        print(f"Error: {e}")

def start_afk_remover():
    activity = bs.get_foreground_host_activity()
    if activity is not None:
        with activity.context:
            bs.timer(1, check_afk, repeat=True)
            print("AFK Remover Started")
        return True
    return False

def activity_checker():
    if start_afk_remover():
        return
    else:
        print("No foreground host activity found, will check again.")
        bs.timer(check_interval, activity_checker, repeat=True)
        

