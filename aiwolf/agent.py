#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/16 16:44:54
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


from aiwolf.core import Role


class IAgent:
    
    def __init__(self, name) -> None:
        self.name=name
    

class IWerewolfAgent(IAgent):
    
    def speak(self) -> str:
        raise NotImplementedError
    
    def vote(self) -> str:
        raise NotImplementedError
    
    
    def observe(self):
        raise NotImplementedError
    
    def assign(self, role:Role):
        raise NotImplementedError
    
    
    
    
class HumanWerewolfAgent(IWerewolfAgent):
    
    
    def speak(self):
        message = input("请输入你的发言：")
        return message
    
    
    def vote(self):
        message = input("请输入你的投票：")
        raise message
    
    
    def observe(self):
        raise NotImplementedError
    
    
    
    