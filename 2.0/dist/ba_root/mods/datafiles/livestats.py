import babase as ba
import bascenev1 as bs
import json
import threading
import _bascenev1 as _bs
from babase._general import Call

class ChatSaver(object):
    def start(self):
        # Set up timers for periodic execution of methods
        self.t1 = bs.AppTimer(2, Call(self.save_chat), repeat=True)
        self.t2 = bs.AppTimer(2, Call(self.player_save), repeat=True)
        self.t3 = bs.AppTimer(1, Call(self.check_ban), repeat=True)

    def save_chat(self):
        try:
            file_path = ba.env()["python_directory_user"] + "/logs/chat.log"
            msgs = bs.get_chat_messages()
            with open(file_path, "r+") as f:
                data = f.readlines()
                for msg in msgs:
                    if msg + "\n" not in data:
                        f.write(msg + "\n")
        except Exception as e:
            print(f"Error in save_chat: {e}")

    def player_save(self):
        try:
            player_file = ba.env()["python_directory_user"] + "/logs/players.log"
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
        except Exception as e:
            print(f"Error in player_save: {e}")

    def check_ban(self):
        ban_path = ba.env()["python_directory_user"] + "/datafiles/staff.json"
        print(f"Ban path: {ban_path}")  # Debugging output
        try:
            with open(ban_path, "r") as f:
                data = json.load(f)
            print(f"Data loaded: {data}")  # Debugging output
        except FileNotFoundError:
            print(f"File not found: {ban_path}")
            return
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return
        except Exception as e:
            print(f"Unexpected error: {e}")
            return

        bannedIDS = data.get("banned", {}).get("pb", [])
        for i in bs.get_game_roster():
            pbid = i["account_id"]
            if pbid in bannedIDS:
                cid = int(i["client_id"])
                ds = i["display_string"]
                bs.chatmessage(f"{ds} You Are Banned")
                bs.disconnect_client(cid)

