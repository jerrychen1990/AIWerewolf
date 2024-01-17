#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/16 16:44:54
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


import random
from aiwolf.core import Role, Action
from snippets.logs import getlog
from snippets.utils import jload
from agit.backend.zhipuai_bk import call_llm_api

logger = getlog(env="DEV", name=__name__)

class IAgent:
    def __init__(self, name:str) -> None:
        self.name=name

    

class IWerewolfAgent(IAgent):


    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.role:Role = None
        self.memory:dict = dict()
        self.env_info:dict=dict()
    
    def refresh(self):
        self.role=None
    
    def acknowledge(self, **kwargs):
        self.env_info.update(**kwargs)
            
    def speak(self) -> str:
        raise NotImplementedError
    
    def vote(self) -> str:
        raise NotImplementedError
    
    def kill(self) -> str:
        if not self.role or self.role!=Role.WEREWOLF:
            raise ValueError("You are not a werewolf! you cannot kill")
            
    def observe(self, action:Action):
        raise NotImplementedError
    
    def assign(self, role:Role):
        self.role=role
    
    def __str__(self):
        return f"{self.name}[{self.role}]"
    
    def __repr__(self) -> str:
        return str(self)
    
    
class RandomWerewolfAgent(IWerewolfAgent):
    
    def speak(self) -> str:
        message = f"{self.name}" + "_" + str(random.randint(0,100))
        logger.info(f"{self} speak {message}")
        return message
    
    def vote(self) -> str:
        vote = random.choice(self.env_info["alive_player_names"])
        logger.info(f"{self} vote {vote}")
        return vote
    
    def kill(self) -> str:
        super().kill()
        to_kill = random.choice(self.env_info["alive_player_names"])
        logger.info(f"{self} choose to kill {to_kill}")
        return to_kill
        
    def observe(self, action:Action):
        logger.info(f"{self.name}[{self.role.value}] observe action:{action}")    
    
    
    
    
class HumanWerewolfAgent(IWerewolfAgent):
            
    def speak(self):
        message = input("请输入你的发言：")
        return message
    
    
    def vote(self):
        message = input("请输入你的投票：")
        raise message
    
    def observe(self, action:Action):
        logger.info(f"{self.name} observe action:{action}")    
        
    def kill(self) -> str:
        super().kill()
        message = input("请输入你的杀人目标：")
        return message        
        
        
        
class LLMWerewolfAgent(IWerewolfAgent):
    def __init__(self, model:str, prompt_file_path:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.prompts = jload(prompt_file_path)
        self.system = ""
        self.memory["actions"]=[]
    
    
    def speak(self) -> str:
        prompt = self.prompts["speak"]
        message = call_llm_api(model=self.model, prompt=prompt, system=self.system, stream=False)
        return message
    
    def vote(self) -> str:
        prompt = self.prompts["vote"]
        message = call_llm_api(model=self.model, prompt=prompt, system=self.system, stream=False)
        vote = message        
        logger.info(f"{self} vote {vote}")
        return vote
    
    def kill(self) -> str:
        super().kill()
        
        prompt = self.prompts["kill"]
        message = call_llm_api(model=self.model, prompt=prompt, system=self.system, stream=False)
        to_kill = message        
        logger.info(f"{self} choose to kill {to_kill}")
        return to_kill
        
    def observe(self, action:Action):
        self.memory["actions"].append(action)
        logger.info(f"{self.name}[{self.role.value}] observe action:{action}")    

    
    
    