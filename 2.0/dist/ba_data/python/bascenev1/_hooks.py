# Released under the MIT License. See LICENSE for details.
#
"""Snippets of code for use by the c++ layer."""
# (most of these are self-explanatory)
# pylint: disable=missing-function-docstring
from __future__ import annotations

from typing import TYPE_CHECKING

import babase

import _bascenev1

import json

if TYPE_CHECKING:
    from typing import Any

    import bascenev1


def launch_main_menu_session() -> None:
    assert babase.app.classic is not None

    _bascenev1.new_host_session(babase.app.classic.get_main_menu_session())


def get_player_icon(sessionplayer: bascenev1.SessionPlayer) -> dict[str, Any]:
    info = sessionplayer.get_icon_info()
    return {
        'texture': _bascenev1.gettexture(info['texture']),
        'tint_texture': _bascenev1.gettexture(info['tint_texture']),
        'tint_color': info['tint_color'],
        'tint2_color': info['tint2_color'],
    }


def filter_chat_message(msg: str, client_id: int) -> str | None:
    import datafiles.chatcmd as cmd
    import datafiles.votinghandler as vh
    acid = ""
    displaystring = ""
    currentname = ""
    filepath = babase.env()["python_directory_user"] + "/datafiles/staff.json"
    f = open(filepath, "r")
    data = json.load(f)
    muteids = data["muted"]["pb"]
    f.close()
    command = msg.split(' ')

    for i in _bascenev1.get_game_roster():
        if i['client_id'] == client_id:
            acid = i['account_id']
            try:
                currentname = i['players'][0]['name_full']
            except:
                currentname = "<in-lobby>"
            displaystring = i['display_string']
    
    if msg in ["!end", "Y", "N"]:
        if msg == "!end"
            print("Vote Started")
            vh.start_vote(client_id)
        else:
            vh.handle_votes(client_id, msg)
    elif (str(command[0])).startswith('/') :
        cmd.Cmd(msg, client_id)

    elif acid in muteids:
        _bascenev1.broadcastmessage("Sorry! You Are Muted", transient=True, color=(1,0,0), clients=client_id)
        return None

    elif data["serverdata"]["chatmuted"]:
        _bascenev1.broadcastmessage("ServerChat Is Muted", transient=True, color=(1,0,0), clients=[client_id])
        return None

    return msg

def local_chat_message(msg: str) -> None:
    classic = babase.app.classic
    assert classic is not None
    party_window = (
        None if classic.party_window is None else classic.party_window()
    )

    if party_window is not None:
        party_window.on_chat_message(msg)
