import babase as ba 
import bascenev1 as bs 
from bascenev1 import chatmessage as cmsg, broadcastmessage as bmsg
import time

players = []
session = bs.get_foreground_host_session
afk_cd = 15
check_interval = 1000  # Check every second

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

    
    host_activity = bs.get_foreground_host_activity()
    for player in host_activity.players:
        last_input = int(player.actor._last_input_time)
        cid = player.sessionplayer.inputdevice.client_id
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
def start():
    if bs.get_foreground_host_session() is not None:
        with bs.get_foreground_host_session().context:
            bs.timer(check_interval, check_afk, repeat=True)
            print("Afk Remover Started")
