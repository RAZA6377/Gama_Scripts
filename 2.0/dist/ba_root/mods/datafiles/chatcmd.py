import babase as ba
import bascenev1 as bs
import _babase as _ba
import _bascenev1 as _bs
import os , json
from bascenev1 import broadcastmessage as bmsg
from bascenev1 import chatmessage as cmsg


def error(msg, clientID):
    bmsg(msg, clients=[clientID], transient=True, color = (1,0,0))
    
def accept_msg(msg, clientID):
    bmsg(msg, clients=[clientID], transient=True, color = (0,1,1))
    

filepath = ba.env()["python_directory_user"] + "/datafiles/staff.json"
f = open(filepath, "r")
data = json.load(f)
f.close()
no_perms = "You Dont Have Permission To Use This Command"
    
class Cmd(object):
    def __init__(self, msg, clientID):
        splitmsg = msg.split(' ')
        self.command = splitmsg[0][1:]
        self.arg = splitmsg[1:]
        self.clientID = clientID
        self.activity = bs.get_foreground_host_activity()
        self.players = bs.get_foreground_host_activity().players
        self.run()

    def run(self):
        if hasattr(self, self.command):
            if self.activity is not None:
                with self.activity.context:
                    exec(f'self.{self.command}()')

    def pidfromnick(self, nick):
        p = bs.get_foreground_host_activity().players
        for i in p:
            name = i.getname()
            if name.lower().find(nick.lower()) != -1:
                return p.index(i)
        bs.chatmessage('player not found')
        return None
                
    def clientidfromnick(self, nick):
        client_id = None
        for i in bs.get_game_roster():
            if len(i['players']) > 0:
                name = i['players'][0]['name_full']
            else:
                name = i['display_string']
            if name.lower().find(nick.lower()) != -1:
                client_id = i['client_id']
                break
        if client_id == None: error("User Not Found", self.clientID)
        return client_id
        
        
    def get_player_info(self, clientID):
        clientID = int(clientID)
        info = {}
        for i in bs.get_game_roster():
            if i['client_id'] == clientID:
                info['ds'] = i['display_string']
                info['aid'] = i['account_id']
                info['p'] = i['players']
                break
        return info
        
        
    
    def end(self):
        global data
        pbid = self.get_player_info(self.clientID)["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.activity is not None:
                self.activity.end_game()
                accept_msg("Command Accepted", self.clientID)
                bmsg("Ended This Activity",color=(1,0,1))
            else:
                error("Currently No Activity Ongoing", self.clientID)
            
        else:
            error(no_perms, self.clientID)

    def mp(self):
        global data
        pbid = self.get_player_info(self.clientID)["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Please Provide A Number", self.clientID)
            else:
                size = int(self.arg[0])
                bs.set_public_party_max_size(size)
                bs.get_foreground_host_session().max_players = size
                accept_msg("Command Accepted", self.clientID)
                bmsg(f"Maxplayers Set To {size}",color = (1,0,1))
            
        else:
            error(no_perms, self.clientID)
    
    def list(self):
        global data
        pbid = self.get_player_info(self.clientID)["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            string = u"{0:^16}{1:^10}{2:^16}\n------------------------------------------------------------------------------\n".format('Name','PlayerID','ClientID')
            for i in bs.get_foreground_host_activity().players:
                name = i.getname(True, True)
                pid = bs.get_foreground_host_activity().players.index(i)
                cid = self.clientidfromnick(name)
                string += u"{0:^16}{1:^10}{2:^16}\n".format(name, pid, cid)
            bmsg(string, transient=True, color=(1, 0, 1), clients=[self.clientID])  
        else:
            error(no_perms, self.clientID)


    def kick(self):
        execinfo = self.get_player_info(self.clientID)
        pbid = execinfo["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Provide Player ClientID Or Name", self.clientID)
            else:
                try:
                    clientid = int(self.arg[0])
                except:
                    name = str(self.arg[0])
                    clientid = self.clientidfromnick(name)
                playerinfo = self.get_player_info(clientid)
                pid = playerinfo["aid"]
                if pid in data["owner"] or pid in data["admin"]:
                    error("Owner And Admins Can\'t Be Kicked", self.clientID)
                else:
                    _bs.disconnect_client(clientid)
                    accept_msg(f"{playerinfo['ds']} Successfully Kicked", self.clientID)
                    bmsg(f"{playerinfo['ds']} Has Been Kicked By {execinfo['ds']}",color=(1,0,1))
        else:
            error(no_perms, self.clientID)

    def ban(self):
        global filepath
        execinfo = self.get_player_info(self.clientID)
        pbid = execinfo["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Provide Player ClientID Or Name", self.clientID)
            else:
                try:
                    clientid = int(self.arg[0])
                except:
                    name = str(self.arg[0])
                    clientid = self.clientidfromnick(name)
                playerinfo = self.get_player_info(clientid)
                pid = playerinfo["aid"]
                if pid in data["owner"]["pb"] or pid in data["admin"]["pb"]:
                    error("Owner And Admins Can\'t Be Banned", self.clientID)
                elif pid in data["banned"]["pb"]:
                    error("User Already Banned", self.clientID)
                else:
                    cmsg(f"{playerinfo['ds']} Has Been Banned By {execinfo['ds']}")
                    _bs.disconnect_client(clientid)
                    accept_msg(f"{playerinfo['ds']} Successfully Banned", self.clientID)
                    bmsg(f"{playerinfo['ds']} Has Been Banned By {execinfo['ds']}",color=(1,0,1))
                    data["banned"]["pb"].append(playerinfo['aid'])
                with open(filepath, "w") as f:
                    
                    try:
                        
                        print(f"Added {playerinfo['ds']} To Ban List")
                        json.dump(data, f, indent=4)
                    except Exception as e:
                        print(e)
        else:
            error(no_perms, self.clientID)

    def unban(self):
        global filepath
        execinfo = self.get_player_info(self.clientID)
        pbid = execinfo["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Provide Player ClientID Or Name", self.clientID)
            else:
                try:
                    clientid = int(self.arg[0])
                except:
                    name = str(self.arg[0])
                    clientid = self.clientidfromnick(name)
                playerinfo = self.get_player_info(clientid)
                pid = playerinfo["aid"]
                
                if pid not in data["banned"]["pb"]:
                    error("User Is Not Banned", self.clientID)
                else:
                    cmsg(f"{playerinfo['ds']} Has Been Unbanned By {execinfo['ds']}")
                    
                    accept_msg(f"{playerinfo['ds']} Successfully Unbanned", self.clientID)
                    bmsg(f"{playerinfo['ds']} Has Been Unbanned By {execinfo['ds']}",color=(1,0,1))
                    data["banned"]["pb"].remove(playerinfo['aid'])
                with open(filepath, "w") as f:
                    
                    try:
                        print(f"Added {playerinfo['ds']} To Ban List")
                        json.dump(data, f, indent=4)
                    except Exception as e:
                        print(e)
        else:
            error(no_perms, self.clientID)

    def rm(self):
        pbid = self.get_player_info(self.clientID)["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Use /rm all or /rm playerid", self.clientID)
            elif self.arg[0] == "all":
                for i in bs.get_foreground_host_session().sessionplayers:
                    i.remove_from_game()
                bmsg("Removed Everyone")
            else:
                try:
                    pid = int(self.arg[0])
                except:
                    name = str(self.arg[0])
                    pid = self.playeridfromnick(name)
                players = bs.getsession().sessionplayers
                players[pid].remove_from_game()
                name = players[pid].getname(True, True)
                accept_msg(f"Successfully Removed", self.clientID)
                bmsg(f"{name} Removed From Game", self.clientID)
        else:
            error(no_perms, self.clientID)
 
                 
    def addadmin(self):
        global filepath
        execinfo = self.get_player_info(self.clientID)
        pbid = execinfo["aid"]
        if pbid in data["owner"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Provide Player ClientID or Name", self.clientID)
            else:
                try:
                    clientid = int(self.arg[0])
                except:
                    name = str(self.arg[0])
                    clientid = self.clientidfromnick(name)
                playerinfo = self.get_player_info(clientid)
                pid = playerinfo["aid"]
                if pid in data["admin"]["pb"]:
                    error("Player Is Already An Admin", self.clientID)
                else:
                    accept_msg(f"{playerinfo['ds']} Is Now An Admin", self.clientID)
                    bmsg(f"{playerinfo['ds']} Is Added To Admin List By {execinfo['ds']}",color=(1,0,1))
                    data["admin"]["pb"].append(playerinfo['aid'])
                with open(filepath, "w") as f:
                    try:
                        print(f"Added {playerinfo['ds']} To Admin List")
                        json.dump(data, f, indent=4)
                    except Exception as e:
                        print(e)
        else:
            error(no_perms, self.clientID)                    

    def rmadmin(self):
        global filepath
        execinfo = self.get_player_info(self.clientID)
        pbid = execinfo["aid"]
        if pbid in data["owner"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Provide Player ClientID or Name", self.clientID)
            else:
                try:
                    clientid = int(self.arg[0])
                except:
                    name = str(self.arg[0])
                    clientid = self.clientidfromnick(name)
                playerinfo = self.get_player_info(clientid)
                pid = playerinfo["aid"]
                if pid not in data["admin"]["pb"]:
                    error("Player Is Not An Admin", self.clientID)
                else:
                    accept_msg(f"{playerinfo['ds']} Removed From Admins", self.clientID)
                    bmsg(f"{playerinfo['ds']} Removed From Admins By {execinfo['ds']}",color=(1,0,1))
                    data["admin"]["pb"].remove(playerinfo['aid'])
                with open(filepath, "w") as f:
                    try:
                        print(f"Removed {playerinfo['ds']} From Admin List")
                        json.dump(data, f, indent=4)
                    except Exception as e:
                        print(e)
        else:
            error(no_perms, self.clientID)                    
                

    def sm(self):
        global data
        pbid = self.get_player_info(self.clientID)["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Use /sm on/off To Use This Cmd", self.clientID)
            elif self.arg[0] == "on":
                bs.get_foreground_host_activity().globalsnode.slow_motion = True
                accept_msg("Slowmode Turned On", self.clientID)
                bmsg("Slowmode Turned On",color=(1,0,1))
            elif self.arg[0] == "off":
                bs.get_foreground_host_activity().globalsnode.slow_motion = False
                accept_msg("Slowmode Turned Off", self.clientID)
                bmsg("Slowmode Turned Off",color=(1,0,1))
            else:
                error("Not A Valid Argument", self.clientID)
            
        else:
            error(no_perms, self.clientID)

        

    def gp(self):
        global data
        pbid = self.get_player_info(self.clientID)["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Provide A Player Id Or Client Id", self.clientID)
            else:
                try:
                    pid = int(self.arg[0])
                except:
                    name = int(self.arg[0])
                    pid = self.pidfromnick(name)
                index = 1
                players = bs.get_foreground_host_session().sessionplayers
                profiles = players[pid].inputdevice.get_player_profiles()
                for i in profiles:
                    cmsg(f"{index} • {i}")
                    index += 1
                accept_msg("Profile Revealed", self.clientID)
                
            
        else:
            error(no_perms, self.clientID)

    def mute(self):
        global filepath
        execinfo = self.get_player_info(self.clientID)
        pbid = execinfo["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Provide Player ClientID Or Name", self.clientID)
            else:
                try:
                    clientid = int(self.arg[0])
                except:
                    name = str(self.arg[0])
                    clientid = self.clientidfromnick(name)
                playerinfo = self.get_player_info(clientid)
                pid = playerinfo["aid"]
                if pid in data["owner"]["pb"] or pid in data["admin"]["pb"]:
                    error("Owner And Admins Can\'t Be Muted", self.clientID)
                elif pid in data["muted"]["pb"]:
                    error("User Already Muted", self.clientID)
                else:
                    cmsg(f"{playerinfo['ds']} Has Been Muted By {execinfo['ds']}")
                    
                    accept_msg(f"{playerinfo['ds']} Successfully Muted", self.clientID)
                    bmsg(f"{playerinfo['ds']} Has Been Muted By {execinfo['ds']}",color=(1,0,1))
                    data["muted"]["pb"].append(playerinfo['aid'])
                with open(filepath, "w") as f:
                    try:
                        print(f"Added {playerinfo['ds']} To Mute List")
                        json.dump(data, f, indent=4)
                    except Exception as e:
                        print(e)
        else:
            error(no_perms, self.clientID)

    def unmute(self):
        global filepath
        execinfo = self.get_player_info(self.clientID)
        pbid = execinfo["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            if self.arg == []:
                error("Provide Player ClientID Or Name", self.clientID)
            else:
                try:
                    clientid = int(self.arg[0])
                except:
                    name = str(self.arg[0])
                    clientid = self.clientidfromnick(name)
                playerinfo = self.get_player_info(clientid)
                pid = playerinfo["aid"]
                
                if pid not in data["muted"]["pb"]:
                    error("User Is Not Muted", self.clientID)
                else:
                    cmsg(f"{playerinfo['ds']} Has Been Unmuted By {execinfo['ds']}")
                    
                    accept_msg(f"{playerinfo['ds']} Successfully Unmuted", self.clientID)
                    bmsg(f"{playerinfo['ds']} Has Been Unmuted By {execinfo['ds']}",color=(1,0,1))
                
                    data["muted"]["pb"].remove(playerinfo['aid'])
                with open(filepath, "w") as f:
                    try:
                        print(f"Removed {playerinfo['ds']} From Mute List")
                        json.dump(data, f, indent=4)
                    except Exception as e:
                        print(e)
        else:
            error(no_perms, self.clientID)

    def quit(self):
        global data
        pbid = self.get_player_info(self.clientID)["aid"]
        if pbid in data["owner"]["pb"] or pbid in data["admin"]["pb"] or self.clientID == -1:
            accept_msg("Command Accepted", self.clientID)
            cmsg("Restarting Server")
            ba.quit()
        else:
            error(no_perms, self.clientID)

    
