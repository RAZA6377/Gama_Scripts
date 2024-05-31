import babase as ba
import bascenev1 as bs
import json
import threading
import _bascenev1 as _bs
from babase._general import Call

class ChatSaver(object):
    def start(self):
        self.t1 = bs.AppTimer(2, Call(self.save_chat), repeat=True)
        self.t2 = bs.AppTimer(2, Call(self.player_save), repeat=True)
        self.t3 = bs.AppTimer(1,Call(self.check_ban), repeat = True)
       

    def save_chat(self):
        try:
            file_path = "/home/ubuntu/gs/dist/ba_root/mods/logs/chat.log"
            msgs = bs.get_chat_messages()
            with open(file_path, "r+") as f:
                data = f.readlines()
                for msg in msgs:
                    if msg + "\n" not in data:
                        f.write(msg + "\n")
        except Exception as e:
            print(e)

    def player_save(self):
        player_file = "/home/ubuntu/gs/dist/ba_root/mods/logs/players.log"
        current_roster = bs.get_game_roster()
        
        with open(player_file, "r+") as f:
            existing_data = f.readlines()
            f.seek(0)
            f.truncate()

            for line in existing_data:
                if any(str(player["client_id"]) in line for player in current_roster):
                    f.write(line)

            for item in current_roster:
                display_string = item["display_string"]
                clientid = str(item["client_id"])
                for player in item["players"]:
                    name = player["name"]
                    player_info = f"{display_string:^10} {name:^16} {clientid:^6}\n"
                    if player_info not in existing_data:
                        f.write(player_info)

    def check_ban(self):
        ban_path = "/home/ubuntu/gs/dist/ba_root/mods/datafiles/staff.json"
        with open(ban_path, "r") as f:
            data = json.load(f)

        bannedIDS = data["banned"]["pb"]
        for i in bs.get_game_roster():
            pbid = i["account_id"]
            if pbid in bannedIDS:
                cid = int(i["client_id"])
                ds = i["display_string"]
                bs.chatmessage(f"{ds} You Are Banned")
                bs.disconnect_client(cid)
            else:
                pass
                
 



     
   


   
