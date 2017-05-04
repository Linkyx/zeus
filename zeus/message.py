# -*- coding:utf-8 -*-

import datetime
import requests
import json

from django.shortcuts import render

from utils import logger, render_json, get_users
from models import Task
from constant import LEVEL, STATUS_CHOICES
# 消息相关接口


def message_index(request):
    """
    消息首页
    :param request:
    :return:
    """
    return render(request, 'message.html', {})