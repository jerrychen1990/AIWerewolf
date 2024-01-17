#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/16 17:00:56
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

from enum import Enum
from pydantic import BaseModel

class Role(Enum):
    WEREWOLF="WEREWOLF"
    VILLAGER="VILLAGER"
    SEER="SEER"
    WITCH="WITCH"
    HUNTER="HUNTER"
    ANCIENT="ANCIENT"
    SAVIOR="SAVIOR"
    
    
ROLE2TYPE = {
    Role.WEREWOLF: "BAD",
    Role.VILLAGER: "GOOD",
    Role.SEER: "GOD",
    Role.WITCH: "GOD",
    Role.HUNTER: "GOD",
    Role.ANCIENT: "GOD",
    Role.SAVIOR: "GOD"
}



class ActionType(str, Enum):
    SPEAK="SPEAK"
    VOTE = "VOTE"
    KILLED= "KILLED"
    EXECUTED="EXECUTED"
    
    def __repr__(self) -> str:
        return self.value

class Action(BaseModel):
    agent_name:str
    action_type:ActionType
    data:dict
    

