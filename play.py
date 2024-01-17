#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/16 20:28:16
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

from aiwolf.agent import RandomWerewolfAgent, LLMWerewolfAgent
from aiwolf.core import Role

from aiwolf.game import WerewolfGame

if __name__ == "__main__":
                
    players = [RandomWerewolfAgent(name=f"p{idx+1}") for idx in range(6)]
    game = WerewolfGame(players=players)
    
    
    players = [LLMWerewolfAgent(name=f"p{idx+1}", model="chatglm_6b", prompt_file_path="config/simple_prompt.json") for idx in range(4)]
    roles = [Role.VILLAGER, Role.WEREWOLF, Role.WEREWOLF, Role.VILLAGER]
    game = WerewolfGame(players=players, roles=roles)
    
    winner = game.run()
    print(f"winner is {winner}")

            
    