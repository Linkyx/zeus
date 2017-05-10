# -*- coding:utf-8 -*-
import time
from django.shortcuts import render

from utils import logger, render_json, get_users
from models import Project, ProjectDynamic
from decorators import user_has_project, process_request


def create_dynamic(request, pid, content, title):
    """
    生成项目动态
    :param request:
    :return:
    """
    try:
        ProjectDynamic.objects.create_dynamic(request=request, pid=pid, content=content, title=title)
    except Exception as e:
        logger.error(u"生成项目动态失败", e)
        return False
    return True


def get_project_dynamic(request, pid):
    """
    获取项目动态
    :param request:
    :return:
    """

    try:
        dynamics = ProjectDynamic.objects.filter(project_id=pid)
    except Exception as e:
        logger.error(u"获取项目动态失败", e)
        dynamics = ''

    return dynamics
