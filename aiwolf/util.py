#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/01/18 18:22:08
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''
import logging
import os
from snippets.logs import getlog_detail


BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

def get_log(name: str):
    logger_level = logging.DEBUG
    logger = getlog_detail(name=name, format_type="detail",
                           level=logger_level, do_print=True, print_format_type="raw", print_level=logging.INFO,
                           do_file=True, log_dir=LOG_DIR)
    return logger