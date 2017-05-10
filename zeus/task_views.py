# -*- coding:utf-8 -*-

import datetime
import requests
import json

from django.shortcuts import render

from utils import logger, render_json, get_users, get_all_users
from models import Task
from constant import LEVEL, STATUS_CHOICES
from zeus.decorators import process_request, user_has_project
from zeus.project_dynamic import create_dynamic, get_project_dynamic


@process_request
def task_index(request):
    """
    用户任务首页
    :param request:
    :return:
    """
    return render(request, 'task_user.html', {})


@process_request
@user_has_project
def get_project_task(request, pid):
    """
    获取项目下的任务
    :param request:
    :return:
    """
    # 获取所用用户信息
    users = get_all_users(request)

    try:
        nofinish_tasks = Task.objects.get_task_pid_unfinish(pid=pid)
        finish_tasks = Task.objects.get_task_pid_finish(pid=pid)
    except Exception as e:
        logger.error(u"查询任务失败", e)
        return render_json({'result': False})
    unfinish_task = []
    # 未完成任务
    for tasks in nofinish_tasks:
        name = tasks.name
        finish_time = tasks.finish_time.strftime('%Y-%m-%d')
        owner = tasks.owner
        user = users[int(owner)]
        avatar = user['avatar']
        level = tasks.level
        tid = tasks.pk
        unfinish_task.append({
            'name': name,
            'finish_time': finish_time,
            'avatar': avatar,
            'level': level,
            'tid': tid
        })

    finish_task = []
    # 已完成任务
    for tasks in finish_tasks:
        name = tasks.name
        finish_time = tasks.finish_time.strftime('%Y-%m-%d')
        owner = tasks.owner
        user = users[int(owner)]
        avatar = user['avatar']
        level = tasks.level
        tid = tasks.pk
        finish_task.append({
            'name': name,
            'finish_time': finish_time,
            'avatar': avatar,
            'level': level,
            'tid': tid
        })

    # 获取项目动态
    dynamic_list = []
    dynamics = get_project_dynamic(request=request, pid=pid)
    for dynamic in dynamics:
        owner = dynamic.sender_id
        user = users[int(owner)]
        avatar = user['avatar']
        dynamic_list.append({
            'content': dynamic.content,
            'title': dynamic.title,
            'create_time': dynamic.create_time.strftime('%Y-%m-%d'),
            'avatar': avatar
        })

    return render(request, 'task_project.html', {
        'pid': pid,
        'finish_task': finish_task,
        'unfinish_task': unfinish_task,
        'dynamic_list': dynamic_list
    })


@process_request
def create_task(request):
    """
    创建任务
    :param request:
    :return:
    """
    name = request.POST.get('name', '')
    introduction = request.POST.get('intro', '')
    participant = request.POST.get('part', '')
    finish_time = request.POST.get('finish_time', '')
    begin_time = request.POST.get('begin_time', '')
    level = request.POST.get('level', '')
    project_id = request.POST.get('pid', '')

    if not name:
        return render_json({'result': False, 'message': u'任务名不能为空'})
    if not finish_time:
        finish_time = datetime.datetime.now()
    if not begin_time:
        begin_time = datetime.datetime.now()

    finish_time_temp = datetime.datetime.strptime(finish_time, "%Y-%m-%d").date()

    try:
        task = Task.objects.create_task(request=request, name=name, introduction=introduction, participant=participant,
                                        begin_time=begin_time, finish_time=finish_time_temp, level=level, project_id=project_id)
    except Exception as e:
        logger.error(u'创建任务失败', e)
        return render_json({'result': False, 'messgae': u'创建任务失败'})

    # 生成项目动态
    content = request.session['name'] + u"创建了一条任务——" + name
    title = u"任务创建"
    create_dynamic(request=request, pid=project_id, content=content, title=title)

    return render_json({'result': True, 'message': u"创建任务成功"})


@process_request
def delete_task(request):
    """
    删除任务
    :param request:
    :return:
    """
    tid = request.POST.get('tid', '')

    try:
        task = Task.objects.get(pk=tid)
        count = Task.objects.delete_task(tid=tid)
    except Exception as e:
        logger.error(u"删除任务失败", e)
        return render_json({'result': False, 'message': u"删除任务失败"})

    # 生成项目动态
    content = request.session['name'] + u"删除了一条任务——" + task.name
    title = u"删除任务"
    create_dynamic(request=request, pid=task.project_id, content=content, title=title)

    return render_json({'result': True, 'message': u"删除任务成功"})


@process_request
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

    users = get_users(request)

    data = []
    for task in tasks:
        # 获取用户名
        participant = task.participant.split(',')
        user_name = []
        for id in participant:
            user = users[int(id)]
            user_name.append(user['name'])

        data.append({
            'task_name': task.name,
            'task_introduction': task.introduction,
            'task_participant': user_name,
            'task_create_time': task.create_time.strftime('%Y-%m-%d'),
            'task_finish_time': task.finish_time.strftime('%Y-%m-%d'),
            'task_status': STATUS_CHOICES[int(task.status)],
            'level': LEVEL[int(task.level)],
        })

    return render_json({'result': True, 'data': data})


@process_request
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