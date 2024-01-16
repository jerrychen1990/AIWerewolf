#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/16 17:00:56
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

from enum import Enum

class Role(Enum, str):
    WOLF="WOLF"
    


class Action(Enum, str):
    SPEAK="SPEAK"
    VOTE = "VOTE"



