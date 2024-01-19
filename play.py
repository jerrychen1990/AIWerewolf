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
    
    names = ["张伟","王伟","李伟","王丽","李静","李娜"]
    
    roles = [Role.WEREWOLF, Role.WEREWOLF, Role.VILLAGER, Role.VILLAGER, Role.VILLAGER]

    model = "glm-4"
    model = "glm-3-turbo"

    
    players = [LLMWerewolfAgent(name=name, model=model) for name in names[:len(roles)]]
    game = WerewolfGame(players=players, roles=roles)
    
    winner = game.run()
    print(f"winner is {winner}")

            
    