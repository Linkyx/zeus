# -*- coding:utf-8 -*-
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
import requests
import re

from decorators import process_request
from models import Project
from utils import render_json, get_users, refresh_user_session, logger, get_all_users


def home(request):
    """
    首页
    :param request:
    :return:
    """
    # 已登录
    status = 1
    try:
        user = request.session['id']

    # session中无user信息
    except KeyError:
        # 未登录
        status = -1
    return render(request, 'home.html', {
        'status': status
    })


@process_request
def index(request):
    """
    项目首页，显示项目信息
    :param request:
    :return:
    """
    part_projects_res = Project.objects.get_user_part_project(request=request)
    owner_projects_res = Project.objects.get_user_owner_project(request=request)

    # 获取所用用户信息
    users = get_users(request)
    # 获取拥有的项目
    owner_project = []
    for project in owner_projects_res:
        pid = project.pk
        name = project.name
        logo = project.logo
        intro = project.introduction
        avatar = request.session['avatar']
        owner_project.append({
            'pid': pid, 'name': name,
            'logo': logo, 'intro': intro,
            'avatar': avatar,
            'owner': request.session['name']
        })

    # 获取参与的项目
    part_project = []
    for project in part_projects_res:
        pid = project.pk
        name = project.name
        logo = project.logo
        intro = project.introduction
        owner = project.owner
        user = users[int(owner)]
        avatar = user['avatar']
        owner = user['name']
        part_project.append({
            'pid': pid,
            'name': name,
            'logo': logo,
            'intro': intro,
            'avatar': avatar,
            'owner': owner
        })

    return render(request, 'index.html', {
        'owner_project': owner_project,
        'part_project': part_project
    })


@process_request
def user_info(request):
    """
    用户信息页面
    :param request:
    :return:
    """
    return render(request, 'user_info.html', {
    })


@process_request
def get_all_user(request):
    """
    获取出当前用户外所有用户
    :param request:
    :return:
    """
    user_info = get_users(request)
    user_list = []
    for id, user in user_info.items():
        user_list.append({'id': id, 'text': user['name']})

    return render_json({'result': True, 'message': user_list})


@process_request
def get_full_user(request):
    """
        获取出当前用户外所有用户
        :param request:
        :return:
        """
    user_info = get_all_users(request)
    user_list = []
    for id, user in user_info.items():
        user_list.append({'id': id, 'text': user['name']})

    return render_json({'result': True, 'message': user_list})


@process_request
def change_user_info(request):
    """
    修改用户信息
    :param request:
    :return:
    """
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('phone', '')
    job = request.POST.get('job', '')
    workplace = request.POST.get('workplace', '')
    qq = request.POST.get('qq', '')
    wechat = request.POST.get('wechat', '')

    m = re.match(r'^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$', email)
    if not m:
        return render_json({'result': False, 'message': u'请检查邮箱格式'})

    p = re.match(r'^1[34578]\d{9}$', phone)
    if not p:
        return render_json({'result': False, 'message': u'请检查手机号格式'})

    payload = {
        'access_token': request.session['token'],
        'name': name,
        'phone': phone,
        'qq': qq,
        'email': email,
        'job': job,
        'workplace': workplace,
        'wechat': wechat
        }
    try:
        res = requests.put('https://api.xiyoulinux.org/users/' + str(request.session['id']), data=payload)
        user_msg = json.loads(res.text)
        if 'error' in user_msg:
            message = u'更新用户信息失败'
            return render_json({'result': False, 'message':  message})
        # 刷新session信息
        refresh_user_session(request, user_msg)
    except Exception as e:
        logger.error(u'更新用户信息失败', e)
        return render_json({'result': False, 'message': u'更新用户信息失败'})
    return render_json({'result': True, 'data': user_msg})
