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
    WEREWOLF="狼人"
    VILLAGER="村民"
    SEER="预言家"
    WITCH="女巫"
    HUNTER="猎人"
    ANCIENT="长老"
    SAVIOR="守卫"
    
    
ROLE2GROUP = {
    Role.WEREWOLF: "狼",
    Role.VILLAGER: "民",
    Role.SEER: "神",
    Role.WITCH: "神",
    Role.HUNTER: "神",
    Role.ANCIENT: "神",
    Role.SAVIOR: "神"
}



class ActionType(str, Enum):
    SPEAK="发言"
    VOTE = "投票"
    KILLED= "被杀死"
    EXECUTED="被处决"
    
    def __repr__(self) -> str:
        return self.value

class Action(BaseModel):
    agent_name:str
    action_type:ActionType
    data:dict
    
    def to_str(self):
        if self.action_type == ActionType.SPEAK:
            return f"{self.agent_name} 发言: {self.data['message']}"
        elif self.action_type == ActionType.VOTE:
            return f"{self.agent_name} 投票给 {self.data['to_vote']}"
        elif self.action_type == ActionType.KILLED:
            return f"{self.agent_name} 被杀死"
        elif self.action_type == ActionType.EXECUTED:
            return f"{self.agent_name} 被处决"
        return ""
        
    

