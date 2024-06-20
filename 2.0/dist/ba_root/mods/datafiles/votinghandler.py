import bascenev1 as bs
import babase as ba
import time

# Made by RaZa

vote_started = False  # Vote start variable
voters = []  # Voters list
ongoing_vote = []  # Last vote which is running
last_vote_end = 0  # When was last vote ended
vote_cooldown = 20  # Voting cooldown

def error(msg, cid: int):
    bs.broadcastmessage(msg, color=(1, 0, 0), transient=True, clients=[cid])

def success(msg, cid: int):
    bs.broadcastmessage(msg, color=(1, 0, 1), transient=True, clients=[cid])

def get_player_info(clientID):
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
    global vote_started
    global voters
    global last_vote_end
    
    last_vote = ongoing_vote[0]
    print(last_vote)
    if last_vote == "quit":
        bs.broadcastmessage("Restarting Server", color=(0, 1, 0))
        ba.quit()
    elif last_vote == "maxplayer":
        limit = bs.get_foreground_host_session().max_players
        bs.get_foreground_host_session().max_players = limit + 1
        bs.set_public_party_max_size = limit + 1
        bs.broadcastmessage(f"Set Maxplayers Size To {limit}", color=(1, 0, 1))
    elif last_vote == "end":
        with bs.get_foreground_host_activity().context:
            bs.get_foreground_host_activity().end_game()
            bs.broadcastmessage("Ending Current Activity", color=(1, 0, 1))
        
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
    current_time = int(time.time())
    
    avail_votes = ["end", "quit", "maxplayer"]  # Available Votes
    if msg in avail_votes:  # if msg is one of the available votes
        if vote_started:  # check if any vote is ongoing
            current_vote = ongoing_vote[0] if ongoing_vote else None
            error(f"A Vote For {current_vote} Is Ongoing", client_id)
        elif current_time <= last_vote_end + vote_cooldown:  # check cooldown
            remain_time = last_vote_end + vote_cooldown - current_time
            error(f"Vote Is On Cooldown. Try Again After {remain_time}s", client_id)
        elif len(bs.get_game_roster()) <= 1:
            error("Not Enough Players To Start A Vote", client_id)
        else:
            vote_started = True
            ongoing_vote.append(msg)
            vote_starter = get_player_info(client_id)
            if vote_starter:
                pb = str(vote_starter["aid"])
                voters.append(pb)
                bs.chatmessage(f"A Vote For {msg} Is Started. Type 'Y' To Vote")
            else:
                error("Could not retrieve player info.", client_id)
    else:
        if msg == "Y":  # if vote is started
            if vote_started:
                playerinfo = get_player_info(client_id)
                if playerinfo:
                    pid = str(playerinfo['aid'])
                    if pid in voters:  # if pbid is in voters list send error
                        error("You Have Already Voted", client_id)
                    else:
                        voters.append(pid)
                        success("You Have Successfully Voted", client_id)
                        need_votes = vote_need(len(bs.get_game_roster())) - len(voters)
                        bs.broadcastmessage(f"{need_votes} Votes Are Needed", color=(0, 1, 1))
                        if need_votes <= 0:  # if needed votes are 0 or less
                            bs.broadcastmessage("Vote Successful", color=(0, 1, 1))
                            vote_success()
                else:
                    error("Could not retrieve player info.", client_id)
        else:
            error("No Vote Ongoing", client_id)
            return

def reset():
    global vote_started
    global voters
    global ongoing_vote
    vote_started = False
    voters.clear()
    ongoing_vote.clear()
    print("Vote Reset")
