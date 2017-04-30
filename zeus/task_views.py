# -*- coding:utf-8 -*-

import datetime
import requests
import json

from utils import logger, render_json
from models import Task
from constant import LEVEL, STATUS_CHOICES


def create_task(request):
    """
    创建任务
    :param request:
    :return:
    """
    name = 'test'
    introduction = "dasdasdasda"
    participant = '12,16'
    finish_time = datetime.datetime.now()
    level = 0
    project_id = 1
    try:
        task = Task.objects.create_task(request=request, name=name, introduction=introduction, participant=participant,
                             finish_time=finish_time,level=level, project_id=project_id)
    except Exception as e:
        logger.error(u'创建任务失败', e)
        return render_json({'result': False, 'messgae': u'创建项目失败'})

    return render_json({'result': True, 'message': u"创建项目成功"})


def get_all_task(request):
    """
    获取所有任务
    :param request:
    :return:
    """
    try:
        tasks = Task.objects.get_all_task()
    except Exception as e:
        logger.error(u"获取任务失败", e)
        return render_json({'result': False, 'message': u"获取任务失败"})

    data = []
    for task in tasks:
        # 获取用户名
        participant = task.participant.split(',')
        payload = {'access_token': request.session['token']}
        user_name = []
        for id in participant:
            user = requests.get('https://api.xiyoulinux.org/users/' + id, params=payload)
            user_name.append(json.loads(user.text)['name'])

        data.append({
            'task_name': task.name,
            'task_introduction': task.introduction,
            'task_participant': user_name,
            'task_create_time': task.create_time.strftime('%Y-%M-%d'),
            'task_finish_time': task.finish_time.strftime('%Y-%M-%d'),
            'task_status': STATUS_CHOICES[int(task.status)],
            'level': LEVEL[int(task.level)],
        })

    return render_json({'result': True, 'data': data})


def update_task_user(request):
    """
    更新任务用户
    :param request:
    :return:
    """
    task_id = 1
    participant = '14,12'

    try:
        info = Task.objects.update_task_user(task_id=task_id, participant=participant)
    except Exception as e:
        logger.error(u"更新任务用户信息失败", e)
        return render_json({'result': False, 'message': u'更新任务用户信息失败'})

    return render_json({'result': True, 'message': u"更新任务用户信息成功"})