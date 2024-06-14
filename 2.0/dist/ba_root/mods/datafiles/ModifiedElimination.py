# let's get back to work..
# modules
import bascenev1, babase

# shortcuts?, cause why not.
roster = bascenev1.get_game_roster
chatmessage = bascenev1.chatmessage

# message variables.
cvs_request = "{} is requesting you for a personal conversation. Y or N?"
cvs_request_sent = "Your personal conversation request has been sent to {}."
cvs_expired = "The personal conversation request has been expired."
cvs_accept = "{} has accepted your personal conversation request."
cvs_reject = "{} has rejected your personal conversation request."
cvs_prefix = "The prefix '{}' has been already taken, change it and try again."
cvs_already_connected = "Your personal conversation is already connected with {}."
cvs_already_requested = "You have already requested a person conversation with {}."
cvs_connect = "Your conversation has been connected to {}.\nThe prefix is {}"
cvs_disconnect = "{} has disconnected the conversation."
cvs_disconnect_sent = "Your conversation with {} has been disconnected."

# important variables (such a pain)
cvs_list = {} # it's a dict, so why call it list?
cvs_request_list = {} # because I love lists ;)
cvs_expiry_time = 20 # seconds
command = "/cvs" # you can change it but make sure to add "/"

# helping functions.
# they are enough but we need someone to use them.

def send_message(msg: str, client_id, override=""):
    """ shortcut for sending chat message with less values. """
    if type(client_id) is int:
        if override:
            chatmessage(msg, clients=[client_id], sender_override=override)
            return
        chatmessage(msg, clients=[client_id])
        return
    if override:
        chatmessage(msg, clients=[c for c in client_id], sender_override=override)
        return
    chatmessage(msg, clients=[c for c in client_id])

def grab_name(client_id: int) -> str:
    """ grabs the given name and returns it. """
    for client in roster():
        if client["client_id"] == client_id:
            if client["players"]:
                return client["players"][0]["name"]
            else: return client["display_string"]

def remove_request(prefix: str, sender: int, receiver: int, instant: bool = False) -> None:
    """ ends the person conversation request. """
    if prefix not in cvs_request_list:
        return
    del cvs_request_list[prefix]
    if instant: return
    send_message(cvs_expired, [sender, receiver])

def send_request(prefix: str, sender: int, receiver: int) -> None:
    """ sends the personal conversation request to a specific person. """
    receiver_name = grab_name(receiver)
    sender_name = grab_name(sender)
    
    # we gotta check if the prefix exists or not
    if prefix in cvs_request_list or prefix in cvs_list:
        # the prefix is already in use, fallback.
        send_message(cvs_prefix.format(prefix), sender)
        return
    else:
        data_format = {"sender": sender, "receiver": receiver}
        # seems like the prefix is good-to-go.
        # but what if the person is trying to connect with same person with a different prefix?
        for _prefix in cvs_request_list:
            if cvs_request_list[_prefix] == data_format:
                send_message(cvs_already_requested.format(receiver_name), sender)
                return
        for _prefix in cvs_list:
            if cvs_list[_prefix] == data_format:
                send_message(cvs_already_connected.format(receiver_name), sender)
                return
        cvs_request_list[prefix] = data_format
        # a timer to end the request.
        expire = lambda : remove_request(prefix, sender, receiver)
        bascenev1.AppTimer(cvs_expiry_time, expire)
        send_message(cvs_request.format(sender_name), receiver)
        send_message(cvs_request_sent.format(receiver_name), sender)

def reject_request(prefix: str, sender: int):
    """ rejects a personal conversation request. """
    del cvs_request_list[prefix]
    send_message(cvs_reject, sender)

def accept_request(prefix: str, sender: int, receiver: int) -> None:
    """ accepts the personal conversation request. """
    receiver_name = grab_name(receiver)
    sender_name = grab_name(sender)
    remove_request(prefix, sender, receiver, True)
    cvs_list[prefix] = {"sender": sender, "receiver": receiver}
    send_message(cvs_accept.format(receier_name), sender)
    send_message(cvs_connect.format(sender_name, prefix), receiver)
    
def disconnect_conversation(prefix: str, sender: int, receiver: int) -> None:
    """ disconnects a conversation. """
    receiver_name = grab_name(receiver)
    sender_name = grab_name(sender)
    del cvs_list[prefix]
    send_message(cvs_disconnect.format(sender_name), receiver)
    send_message(cvs_disconnect_sent.format(receiver_name), sender)

orginial_leave = bascenev1._activity.Activity.on_player_leave
def on_player_leave(self, player):
    orginial_leave(self, player)
    client_id = player.inputdevice.client_id
    for prefix in conversation.cvs_list:
        cvr = conversation.cvs_list[prefix]
        if cvr["sender"] == client_id:
            conversation.disconnect_conversation(prefix, client_id, cvr["receiver"])
        elif cvr["receiver"] == client_id:
           conversation.disconnect_conversation(prefix, client_id, cvr["sender"])
    
# main function
# let's cook, shall we?.
def inspect_message(message: str, client_id):
    """ inspects the message. """
    # is it a cvs command?
    if message.startswith('/') and message.split()[0] == command:
        # try and except seems easy to me.
        try:
            receiver = int(message.split()[1])
            prefix = str(message.split()[2])
            send_request(prefix, client_id, receiver)
        except:
            # ahm, some error occured..
            # but we know what that is.
            send_message(f"Usage: {command} <receiver_id> <prefix>\nExample: {command} 125 ?", client_id)
        return
    
    # could it be accept or reject message?
    if message.lower() == "y":
        for prefix in cvs_request_list:
            if cvs_request_list[prefix]["receiver"] == client_id:
                accept_request(prefix, cvs_request_list[prefix]["sender"], client_id)
                return
    elif message.lower() == "n":
        for prefix in cvs_request_list:
            if cvs_request_list[prefix]["receiver"] == client_id:
                reject_request(prefix, cvs_request_list[prefix]["sender"])
                return
    
    # is it disconnect command?
    if message.lower() == "/disconnect":
        for prefix in cvs_list:
            if cvs_list[prefix]["sender"] == client_id or cvs_list[prefix]["receiver"] == client_id:
                disconnect_conversation(prefix, cvs_list[prefix]["sender"], cvs_list[prefix]["receiver"])
                return
    
    prefix = message[0]
    # we don't know if that's a prefix yet.
    if prefix in cvs_list:
        # it's a prefix.
        prefix_list = cvs_list[prefix]
        if not prefix_list["sender"] == client_id and not prefix_list["receiver"] == client_id:
            return message
        client_name = grab_name(client_id)
        override_format = f"{client_name} (P)" # (P) to get informed that it's a private message.
        try:
            message = message[1:]
        except:
            message = ""
        send_message(message, [prefix_list["sender"], prefix_list["receiver"]], override_format)
        return
    return message
