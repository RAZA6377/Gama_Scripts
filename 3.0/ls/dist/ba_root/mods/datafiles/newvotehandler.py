import bascenev1 as bs
import babase as ba
import time

vote_started = False
voters = []
vote_started_on = 0
vote_cooldown = 20

def get_player_info(clientID: int):
    clientID = int(clientID)
    info = {}
    for i in bs.get_game_roster():
        if i['client_id'] == clientID:
            info['ds'] = i['display_string']
            info['aid'] = i['account_id']
            info['p'] = i['players']
            break
    return info

def vote_need(players):
    if players == 2:
        return 2
    elif players == 3:
        return 2
    elif players == 4:
        return 2
    elif players == 5:
        return 3
    elif players == 6:
        return 3
    elif players == 7:
        return 4
    elif players == 8:
        return 4
    elif players == 10:
        return 5
    else:
        return players - 5

def add_voter(clientid: int):
    try:
        playerinfo = get_player_info(clientid)
        if clientid in voters:
            bs.broadcastmessage("You Have Already Voted\nUse 'N' To Remove Vote", color=(1, 0, 0), transient=True, clients=[clientid])
        else:
            voters.append(clientid)
            bs.broadcastmessage("Vote Accepted! Thanks For The Vote\nUse 'N' To Remove Vote", color=(1, 0, 1), transient=True, clients=[clientid])
            total_votes = vote_need(len(bs.get_game_roster()) - 1)
            total_voters = len(voters)
            need_votes = total_votes - total_voters
            if not need_votes:
                end()
                return None                             
            bs.chatmessage(f"{need_votes} More Votes Needed")
            print(f"Voter added: {playerinfo['ds']}, Total Voters: {total_voters}, Votes Needed: {need_votes}")
    except Exception as e:
        print(f"Error in add_voter: {e}")

def remove_voter(clientid: int):
    try:
        playerinfo = get_player_info(clientid)
        if clientid in voters:
            voters.pop(clientid)
            bs.broadcastmessage("Your Vote Is Successfully Removed\nUse 'Y' To Add Vote", color=(1, 0, 1), transient=True, clients=[clientid])
            total_votes = vote_need(len(bs.get_game_roster()) - 1)
            total_voters = len(voters)
            need_votes = total_votes - total_voters
            if not need_votes:
                end()
                return None
            bs.chatmessage(f"{need_votes} More Votes Needed")
            print(f"Voter removed: {playerinfo['ds']}, Total Voters: {total_voters}, Votes Needed: {need_votes}")
        else:
            bs.broadcastmessage("You Haven't Voted Yet\nUse 'Y' To Add Vote", color=(1, 0, 0), transient=True, clients=[clientid])
    except Exception as e:
        print(f"Error in remove_voter: {e}")

def end():
    try:
        bs.chatmessage("End Vote Succeed")
        with bs.get_foreground_host_activity().context:
            bs.get_foreground_host_activity().end_game()
        voters = []
        vote_started = False
    except Exception as e:
        print(e)
        pass

def start_vote(clientid: int, msg):
    global vote_started
    global vote_started_on
    global voters
    global vote_cooldown
    playerinfo = get_player_info(clientid)
    if vote_started:
        bs.broadcastmessage("A Vote Is Already Ongoing", transient=True, clients=[clientid], color=(1, 0, 0))
        return
    now = time.time()
    if now < vote_started_on + vote_cooldown:
        retry_time = int(vote_started_on + vote_cooldown - now)
        bs.broadcastmessage(f"Vote Is On Cooldown. Retry After {retry_time}s", color=(1, 0, 0), transient=True, clients=[clientid])
        return
    if len(bs.get_game_roster()) - 1 == 1:
        bs.broadcastmessage("Not Enough Players To Start A Vote", color=(1, 0, 0), transient=True, clients=[clientid])
        return
    else:
        vote_started = True
        vote_started_on = time.time()
        bs.chatmessage("A Vote For End Is Started\nType 'Y' To Vote")
        voters.append(clientid)
  

def handle_votes(clientid: int, msg):
    global vote_started
    global vote_started_on
    global voters
    global vote_cooldown
    current_players = [player['client_id'] for player in bs.get_game_roster()]
    if vote_started:
        if vote_need(len(current_players)-1) - len(voters) <= 0:
                end()
                return None
        elif msg == "Y":
            add_voter(clientid)
        elif msg == "N":
            remove_voter(clientid)
    else:
        bs.broadcastmessage("No Vote Is Ongoing. Try Running ?end To Start", color=(1, 0, 0), transient=True, clients=[clientid])

def reset():
    
    voters = []
    vote_started = False
    print("Vote Reset")
