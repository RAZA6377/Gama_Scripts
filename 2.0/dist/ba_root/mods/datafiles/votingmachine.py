#  Electronic Voting Machine (EVM) by -mr.smoothy

import time

import _babase
import babase

import bascenev1 as bs

game_started_on = 0

vote_machine = {"end": {"last_vote_start_time": 0, "vote_duration": 50,"min_game_duration_to_start_vote": 5, "vote_cooldown": 10,"voters": []},
"quit": {"last_vote_start_time": 0, "vote_duration": 50,"min_game_duration_to_start_vote": 10, "vote_cooldown": 1000,"voters": []},
"maxplayer": {"last_vote_start_time": 0, "vote_duration": 50,"min_game_duration_to_start_vote": 1, "vote_cooldown": 10,"voters": []}}



def vote(pb_id, client_id, vote_type):
    global vote_machine
    voters = vote_machine[vote_type]["voters"]
    last_vote_start_time = vote_machine[vote_type]["last_vote_start_time"]
    vote_duration = vote_machine[vote_type]["vote_duration"]
    vote_cooldown = vote_machine[vote_type]["vote_cooldown"]
    min_game_duration_to_start_vote = vote_machine[vote_type][
        "min_game_duration_to_start_vote"]

    now = time.time()
    if now > last_vote_start_time + vote_duration:
        voters = []
        vote_machine[vote_type]["last_vote_start_time"] = now
    if now < game_started_on + min_game_duration_to_start_vote:
        bs.broadcastmessage(
            "Game Just Started Try Again In A Few Seconds",
            transient=True,
            color = (1,0,0),
            clients=[client_id])
    if now < last_vote_start_time + vote_cooldown:
        retry_time = int(now) - int(last_vote_start_time) + int(vote_cooldown)
        bs.broadcastmessage(
            f"Command Is On Cooldown Try Again After {retry_time} Seconds",
            transient=True,
            color = (1,0,0),
            clients=[client_id])
        return
    if len(voters) == 0:
        bs.chatmessage(f"A Vote For {vote_type} Is Started")

    # clean up voters list
    active_players = []
    for player in bs.get_game_roster():
        active_players.append(player['account_id'])
    for voter in voters:
        if voter not in active_players:
            voters.remove(voter)
    if pb_id not in voters:
        voters.append(pb_id)
        bs.broadcastmessage(
            f'Vote Accepted, Ask Others To Vote By Writing {vote_type}',
            transient=True,
            color = (1,0,1),
            clients=[client_id])
        if vote_type == 'end':
            update_vote_text(max_votes_required(
                len(active_players)) - len(voters))
        else:
            activity = bs.get_foreground_host_activity()
            if activity is not None:
                with bs.get_foreground_host_activity().context:
                    bs.broadcastmessage(
                        f"{max_votes_required(len(active_players)) - len(voters)} Votes Are Need For {vote_type}",
                        image={"texture": bs.gettexture(
                            "achievementSharingIsCaring"),
                               "tint_texture": bs.gettexture(
                                   "achievementSharingIsCaring"),
                               "tint_color": (0.5, 0.5, 0.5),
                               "tint2_color": (0.7, 0.5, 0.9)},
                        top=True)
    vote_machine[vote_type]["voters"] = voters

    if len(voters) >= max_votes_required(len(active_players)):
        bs.screenmessage(f"{vote_type} Vote Success", color=(0,1,1))
        vote_machine[vote_type]["voters"] = []
        if vote_type == "end":
            try:
                with bs.get_foreground_host_activity().context:
                    bs.get_foreground_host_activity().end_game()
            except:
                pass
        elif vote_type == "maxplayer":
            maxp = bs.get_foreground_host_session().max_players
            setmaxp = int(maxp) + 1
            bs.chatmessage("/mp " + str(setmaxp))
            bs.screenmessage(f"Set Maxplayers Limit To {setmaxp}", color=(0,1,0))
        elif vote_type == "quit":
            bs.chatmessage("Server Is Quiting, Join Again")
            babase.quit()


def reset_votes():
    global vote_machine
    for value in vote_machine.values():
        value["voters"] = []


def max_votes_required(players):
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


def update_vote_text(votes_needed):
    activity = bs.get_foreground_host_activity()
    try:
        activity.end_vote_text.node.text = "{} More Votes Are Need\nTo End This Map".format(votes_needed)
    except:
        with bs.get_foreground_host_activity().context:
            node = bs.newnode('text',
                                           attrs={
                                               'v_attach': 'top',
                                               'h_attach': 'center',
                                               'h_align': 'center',
                                               'color': (0,1,1),
                                               'flatness': 0.5,
                                               'shadow': 0.5,
                                               'position': (-200, -30),
                                               'scale': 0.7,
                                               'text': '{} More Votes Are Need\nTo End This Map'.format(votes_needed)
                                           })
            activity.end_vote_text = node
            bs.timer(20, remove_vote_text)


def remove_vote_text():
    activity = bs.get_foreground_host_activity()
    if hasattr(activity,
               "end_vote_text") and activity.end_vote_text.node.exists():
        activity.end_vote_text.node.delete()
