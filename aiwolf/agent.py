#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/16 16:44:54
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


import random
from tabnanny import verbose
from typing import List
from aiwolf.core import Role, Action
from aiwolf.util import get_log
from snippets.logs import getlog
import config.simple_prompt as prompts
from agit.backend import call_llm_api

logger = get_log(name=__name__)


class IAgent:
    def __init__(self, name: str) -> None:
        self.name = name


class IWerewolfAgent(IAgent):

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.role: Role = None
        self.memory: dict = dict()
        self.env_info: dict = dict()

    def refresh(self):
        self.role = None

    def acknowledge(self, **kwargs):
        self.env_info.update(**kwargs)

    def speak(self) -> str:
        raise NotImplementedError

    def vote(self) -> str:
        raise NotImplementedError

    def kill(self) -> str:
        if not self.role or self.role != Role.WEREWOLF:
            raise ValueError("You are not a werewolf! you cannot kill")

    def observe(self, action: Action):
        raise NotImplementedError

    def assign(self, role: Role):
        self.role = role

    def __str__(self):
        return f"{self.name}[{self.role.value}]"

    def __repr__(self) -> str:
        return str(self)

    def _assert_in_names(self, name: str):
        if name not in self.env_info["alive_player_names"]:
            logger.warning(f"{name} is not in alive players, will random choose one")
            return random.choice(self.env_info["alive_player_names"])
        return name


class RandomWerewolfAgent(IWerewolfAgent):

    def speak(self) -> str:
        message = f"{self.name}" + "_" + str(random.randint(0, 100))
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

    def observe(self, action: Action):
        logger.info(f"{self.name}[{self.role.value}] observe action:{action}")


class HumanWerewolfAgent(IWerewolfAgent):

    def speak(self):
        message = input("请输入你的发言：")
        return message

    def vote(self):
        message = input("请输入你的投票：")
        raise message

    def observe(self, action: Action):
        logger.info(f"{self.name} observe action:{action}")

    def kill(self) -> str:
        super().kill()
        message = input("请输入你的杀人目标：")
        return message


def extract_name(message: str, pattern: str):
    import re
    for item in re.findall(pattern, message):
        return item.strip()
    return message

import logging
# verbose = logging.INFO
# the_logger = logging.getLogger("agit")
the_logger = logger

class LLMWerewolfAgent(IWerewolfAgent):
    def __init__(self, model: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.memory["actions"]:List[Action] = []

    def _build_information(self):
        info = f"你的名字是{self.name}, 你的身份是:{self.role.value}, 你的阵营是{'狼人' if self.role==Role.WEREWOLF else '好人'}"
        all_players = f"其他玩家有：{','.join(self.env_info['alive_player_names'])}"
        partners = self.env_info.get("partners")
        partners = ",".join(partners) if partners else "未知"
        partners = f"你的队友有：{partners}"
        return "\n".join([info, all_players, partners])        
        
        
    def _build_observation(self):
        actions = [e.to_str() for e in self.memory["actions"]]
        return "\n".join(actions)
        
    def _build_system(self):
        information = self._build_information()
        observation = self._build_observation()
        return prompts.system.format(rule=prompts.rule, information=information, observation=observation)

    def speak(self) -> str:
        prompt = prompts.speak
        message = call_llm_api(model=self.model, prompt=prompt, system=self._build_system(), stream=False, logger=the_logger)
        return message

    def vote(self) -> str:
        prompt = prompts.vote.format(names=[e for e in self.env_info["alive_player_names"] if e!=self.name])
        message = call_llm_api(model=self.model, prompt=prompt, system=self._build_system(), stream=False, logger=the_logger)
        logger.debug(f"vote message:[{message}]")

        vote = extract_name(message, prompts.vote_pattern)
        vote = self._assert_in_names(vote)
        # logger.info(f"{self} vote {vote}")
        return vote

    def kill(self) -> str:
        super().kill()
        prompt = prompts.kill.format(names=self.env_info["alive_player_names"])
        message = call_llm_api(model=self.model, prompt=prompt, system=self._build_system(), stream=False, logger=the_logger)
        logger.debug(f"kill message:[{message}]")
        to_kill = extract_name(message, prompts.kill_pattern)
        to_kill = self._assert_in_names(to_kill)
        # logger.info(f"{self} choose to kill {to_kill}")
        return to_kill

    def observe(self, action: Action):
        self.memory["actions"].append(action)
        # logger.debug(f"{self.name}[{self.role.value}] observe action:{action}")
