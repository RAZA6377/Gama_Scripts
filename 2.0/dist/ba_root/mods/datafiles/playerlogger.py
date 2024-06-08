import babase as ba
import bascenev1 as bs
import time

filepath = ba.env()["python_directory_user"] + "/logs/server.log"

orginial_join = bs._activity.Activity.on_player_join

orginial_leave = bs._activity.Activity.on_player_leave

def on_player_join(self, player):
    orginial_join(self, player)
    print("Player Joined")
    try:
        v1id = player.sessionplayer.get_v1_account_id()
        try:
            name = player.sessionplayer.getname(True, False)
        except Exception as e:
            print(e)
            name = "[In-Lobby]"
        with open(filepath, "r+") as f:
            data = f.readlines()
            current_time = int(time.time())
            text = f"<t:{current_time}:R> » [{v1id}](http://bombsquadgame.com/bsAccountInfo?buildNumber=20258&accountID={v1id}) » {name} » Joined Server"
            f.write(text + "\n")
    except Exception as e:
        print(e)
        pass

def on_player_leave(self, player):
    orginial_leave(self, player)
    print("Player Leaved")
    try:
        v1id = player.sessionplayer.get_v1_account_id()
        try:
            name = player.sessionplayer.getname(True, False)
        except Exception as e:
            print(e)
            name = "[In-Lobby]"
        with open(filepath, "r+") as f:
            data = f.readlines()
            current_time = int(time.time())
            text = f"<t:{current_time}:R> » [{v1id}](http://bombsquadgame.com/bsAccountInfo?buildNumber=20258&accountID={v1id}) » {name} » Left Server"
            f.write(text + "\n")
    except Exception as e:
        print(e)
        pass
        


def apply():
    try:
        bs._activity.Activity.on_player_join = on_player_join
        bs._activity.Activity.on_player_leave = on_player_leave
    except Exception as e:
        print(e)
        pass
