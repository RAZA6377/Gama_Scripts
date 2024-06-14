import bascenev1 as bs
import babase as ba
import time

# Made by RaZa


vote_started = False # Vote start variable
voters = [] # Voters list
ongoing_vote = [] # Last vote which is running
last_vote_end = 0 # When was last vote ended
vote_cooldown = 20 # Voting cooldown
current_time = int(time.time()) # current time in seconds

def error(msg, cid: int):
    broadcastmessage(msg, color=(1,0,0), transient=True, clients=[cid])
    
def success(msg, cid: int):
    broadcastmessage(msg, color=(1,0,1), transient=True, clients=[cid])

def get_player_info(clientID):
        clientID = int(clientID)
        info = {}
        for i in _ba.get_game_roster():
            if i['client_id'] == clientID:
                info['ds'] = i['display_string']
                info['aid'] = i['account_id']
                info['p'] = i['players']
                break
        return info

def vote_need(players):
    if players == 2:
        return 1
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

def vote_success():
    global ongoing_vote
    last_vote = ongoing_vote[0]
    if last_vote == "quit":
        bs.broadcastmessage("Restarting Server", color=(0,1,0))
        ba.quit()
    elif last_vote == "maxplayer":
        limit = bs.get_foreground_host_session().max_players # before limit
        bs.get_foreground_host_session().max_players = limit + 1 #after limit
        bs.set_public_party_max_size = limit + 1
        bs.broadcastmessage(f"Set Maxplayers Size To {limit}", color=(1,0,1))
    elif last_vote == "end":
        bs.get_foreground_host_activity().end_game()
        bs.broadcastmessage("Ending Current Activity", color=(1,0,1))
        
    vote_started = False
    voters.clear()
    last_vote_end = int(time.time())
    ongoing_vote.clear()

def check_vote(msg, client_id: int):
    global vote_started
    global voters
    global vote_cooldown
    global last_vote_end
    global ongoing_vote
    global current_time
    avail_votes = ["end", "quit", "maxplayer"] # Available Votes
    if msg in avail_votes: # if msg anyone of Available votes
        if vote_started: # check if any vote is ongoing
            current_vote = ongoing_vote[0] # last vote 
            error(f"A Vote For {current_vote} Is Ongoing", client_id)
        elif current_time <= last_vote_end + vote_cooldown: # check cooldown
            remain_time = last_vote_end + vote_cooldown - current_time
            error(f"Vote Is On Cooldown Try Again After {remain_time}s", client_id)
        else:
            vote_started = True
            # lets save current vote mode to list
            if msg == "end":
                ongoing_vote.append("end")
            elif msg == "quit":
                ongoing_vote.append("quit")
            elif msg == "maxplayer":
                ongoing_vote.append("maxplayer")
            vote_for = ongoing_vote[0]
            bs.broadcastmessage(f"A Vote For {vote_for}\nIs Started\nType \'Y\' To Vote", color=(0,1,0))
            
    else:
        if vote_started: # if vote is started 
            if msg == "Y":
                playerinfo = get_player_info(client_id)
                pid = str(playerinfo['aid'])
                if pid in voters: # if pbid in voters list send error
                    error("You Have Already Voted", client_id)
                    
                else:
                    voters.append(pid) 
                    success("You Have Successfully Voted", client_id)
                    need_votes = len(vote_need(len(bs.get_game_roster()) - 1)) - len(voters) # how many votes needed
                    bs.broadcastmessage(f"{need_votes} Votes Are Needed", color=(0,1,1))
                    if need_votes <= 0: # if need votes is 0 or greater than them xd
                        bs.broadcastmessage("Vote Successfull", color=(0,1,1))
                        vote_success()
        
# Lets Add A Function that reset votes we call this function when a new activity is started
def reset():
    global vote_started
    global voters
    vote_started = False
    voters.clear()
    print("Vote Reseted")