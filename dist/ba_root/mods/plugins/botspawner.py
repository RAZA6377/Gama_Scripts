import babase
import bascenev1
from babase._player import Player
from babase._activity import Activity
from bascenev1.game.elimination import EliminationGame

def modified_on_begin(self):
        import random, babase
        from bascenev1.actor.spazbot import (SpazBotSet, SpazBotDiedMessage, BomberBot,
                                 BomberBotPro, BomberBotProShielded,
                                 BrawlerBot, BrawlerBotPro,
                                 BrawlerBotProShielded, TriggerBot,
                                 TriggerBotPro, TriggerBotProShielded,
                                 ChargerBot, StickyBot, ExplodeyBot)
        try:
            self._bots = SpazBotSet()
            self.botTypes = [BomberBot, BomberBotPro, BomberBotProShielded,
                             BrawlerBot, BrawlerBotPro,
                             BrawlerBotProShielded, TriggerBot,
                             TriggerBotPro, TriggerBotProShielded,
                             ChargerBot, StickyBot, ExplodeyBot
            ]
            def btspawn():
                if len(self.players) == 1:
                    try:
                        if not self._bots.have_living_bots():
                            pt = (self.players[0].actor.node.position[0],
                                  self.players[0].actor.node.position[1] + 2,
                                  self.players[0].actor.node.position[2])
                            self._bots.spawn_bot(random.choice(self.botTypes), pos=pt, spawn_time=0.5)
                    except:
                        pass
                else:
                    self.botTimer = None
                self.botTimer = ba.Timer(1,btspawn,repeat=True)
        except:
            pass
        
Activity.on_begin = modified_on_begin  

def modified_on_player_leave(self, player):
        import random, babase
        from bascenev1.actor.spazbot import (SpazBotSet, SpazBotDiedMessage, BomberBot,
                                 BomberBotPro, BomberBotProShielded,
                                 BrawlerBot, BrawlerBotPro,
                                 BrawlerBotProShielded, TriggerBot,
                                 TriggerBotPro, TriggerBotProShielded,
                                 ChargerBot, StickyBot, ExplodeyBot)
        try:
            self._bots = SpazBotSet()
            self.botTypes = [BomberBot, BomberBotPro, BomberBotProShielded,
                             BrawlerBot, BrawlerBotPro,
                             BrawlerBotProShielded, TriggerBot,
                             TriggerBotPro, TriggerBotProShielded,
                             ChargerBot, StickyBot, ExplodeyBot
            ]
            def btspawn():
                if len(self.players) == 1:
                    try:
                        if not self._bots.have_living_bots():
                            pt = (self.players[0].actor.node.position[0],
                                  self.players[0].actor.node.position[1] + 2,
                                  self.players[0].actor.node.position[2])
                            self._bots.spawn_bot(random.choice(self.botTypes), pos=pt, spawn_time=0.5)
                    except:
                        pass
                else:
                    self.botTimer = None
                    
                self.botTimer = ba.Timer(1,btspawn,repeat=True)
        except:
            pass
            
Activity.on_player_leave = modified_on_player_leave

def _modified_update(self):
        if self._solo_mode:
            # For both teams, find the first player on the spawn order
            # list with lives remaining and spawn them if they're not alive.
            for team in self.teams:
                # Prune dead players from the spawn order.
                team.spawn_order = [p for p in team.spawn_order if p]
                for player in team.spawn_order:
                    assert isinstance(player, Player)
                    if player.lives > 0:
                        if not player.is_alive():
                            self.spawn_player(player)
                            self._update_icons()
                        break

        # If we're down to 1 or fewer living teams, start a timer to end
        # the game (allows the dust to settle and draws to occur if deaths
        # are close enough).
        if len(self._get_living_teams()) < 2:
            if len(self.players) == 1 and self.players[0].lives > 0:
                return
            self._round_end_timer = ba.Timer(0.5, self.end_game)
      
EliminationGame._update = _modified_update      
