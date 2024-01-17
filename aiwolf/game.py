#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/16 16:56:01
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


from collections import defaultdict
import copy
import random
from pydantic import BaseModel
from aiwolf.core import ROLE2TYPE, Action, ActionType, Role
from snippets.logs import getlog
from aiwolf.agent import IWerewolfAgent

logger = getlog("dev", __name__)


class IGame:
    pass



class WerewolfGame(IGame):

    
    def __init__(self, players:list[IWerewolfAgent]=[],        
                 roles:list = [Role.WEREWOLF, Role.WEREWOLF,Role.WITCH, Role.VILLAGER,Role.VILLAGER, Role.SEER],
                 
        ):
        self.players= players
        self.roles=roles
        self.alive_players = copy.copy(self.players)
    
    
    def _assign_role(self):
        random.shuffle(self.players)
        for p, r in zip(self.players, self.roles):
            p.assign(r)
        random.shuffle(self.players)
        logger.info(f"player roles: {[f'{p.name}:[{p.role.value}]' for p in self.players]}")
        
    

    
    def pre_game(self):
        logger.info("初始化游戏...")
        self._check_player()
        for player in self.players:
            player.refresh()        
        self._assign_role()
        self.alive_players = copy.copy(self.players)
        self._broadcast_info(roles=self.roles, alive_player_names = [e.name for e in self.alive_players])
        return self.alive_players
        
        
    def _check_player(self):
        return len(self.roles) == len(self.players) 
    
    
    def is_over(self):
        role_type_dict = defaultdict(int)
        for p in self.alive_players:
            role_type_dict[ROLE2TYPE[p.role]] += 1
        logger.debug(f"{role_type_dict=}")
        if role_type_dict["BAD"] == 0:
            return "GOOD"
        if role_type_dict["GOOD"] == 0 and role_type_dict["GOD"] == 0:
            return "BAD"
        return None
        
        
    def _broadcast_action(self, action:Action):
        for player in self.alive_players:
            player.observe(action=action)
            
    def _broadcast_info(self, **kwargs):
        for player in self.alive_players:
            player.acknowledge(**kwargs)

    def run(self):
        self.pre_game()
        _round = 1
        while True:
            winner =  self.is_over()
            if winner:
                logger.info(f"游戏结束，赢家:{winner}")
                return winner
            name2player = {p.name:p for p in self.alive_players}
            logger.info(f"**************************** 回合:{_round} ****************************")
            
            logger.info("**************************** 狼人阶段 ****************************")
            kill_dict = defaultdict(int)

            for player in self.alive_players:
                if player.role == Role.WEREWOLF:
                    to_kill = player.kill()
                    kill_dict[to_kill] += 1
            logger.debug(f"{kill_dict=}")
            kill_items = sorted(kill_dict.items(), key=lambda x:x[1], reverse=True)    
            logger.debug(f"{kill_items=}")
            for name, num in kill_items:
                if name in set(name2player):
                    p = name2player[name]
                    logger.info(f"{p}被杀死")
                    if p in self.alive_players:                    
                        self.alive_players.remove(name2player[name])    
                        action = Action(agent_name=name, data=dict(), action_type=ActionType.KILLED)
                        self._broadcast_action(action=action)
                        break
            logger.debug(f"current alive players: {self.alive_players}")

            self._broadcast_info(alive_player_names = [e.name for e in self.alive_players])

                                    
            logger.info(f"**************************** 发言阶段 ****************************")
            for player in self.alive_players:
                message = player.speak()
                action = Action(agent_name=player.name, data=dict(message=message), action_type=ActionType.SPEAK)
                self._broadcast_action(action=action)
                
            
            logger.info("**************************** 投票阶段 ****************************")
            vote_dict = defaultdict(int)
            for player in self.alive_players:
                to_vote = player.vote()
                vote_dict[to_vote] += 1
                action = Action(agent_name=player.name, data=dict(to_vote=to_vote), action_type=ActionType.VOTE)
                self._broadcast_action(action=action)

            vote_items = sorted(vote_dict.items(),key=lambda x:x[1], reverse=True)
            logger.debug(f"{vote_items=}")  
            for name, num in vote_items:
                if name in set(name2player):
                    p = name2player[name]
                    if p in self.alive_players:
                        logger.info(f"{p}被处决")
                        self.alive_players.remove(p)    
                        action = Action(agent_name=name, data=dict(), action_type=ActionType.EXECUTED)
                        self._broadcast_action(action=action)
                        break
            logger.debug(f"current alive players: {self.alive_players}")

            self._broadcast_info(alive_player_names = [e.name for e in self.alive_players])

            _round += 1
            

            
            
            
            
        
        
        
        
        
        