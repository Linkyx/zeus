# -*- coding:utf-8 -*-
import time
from django.shortcuts import render

from utils import logger, render_json, get_users
from models import Project
from decorators import user_has_project, process_request


@process_request
# 项目相关接口
def create_project(request):
    """
    创建项目
    :param request:
    :return:
    """
    name = request.POST.get('pro_name', '')
    introduction = request.POST.get('pro_intro', '')
    participant = request.POST.get('pro_part', '')
    img = request.FILES.get('pro_img', '')
    if not name:
        return render_json({'result': False, 'message': u'项目名不能为空'})

    if img:
        import os
        try:
            # 根据时间戳存储图片
            now = int(time.time())
            ext = img.name.split('.')[-1]
            img_first_name = '.'.join(img.name.split('.')[:-1])
            img_name = img_first_name + str(now)
            img_full_name = img_name + '.' + ext
            img_path = os.path.join(os.path.dirname(__file__), 'static/images/', img_full_name)
            with open(img_path, 'wb') as f:
                for item in img.chunks():
                    f.write(item)
        except Exception as e:
            logger.error(u'图片写入失败', e)
            return render_json({'result': False, 'message': u'图片写入失败'})
    else:
        # 默认背景图
        img_full_name = 'cover-internet.jpg'
    try:
        project = Project.objects.create_project(request=request, name=name, introduction=introduction,
                                                 participant=participant, logo='/static/images/' + img_full_name)
    except Exception as e:
        logger.error(u"创建项目失败", e)

    return render_json({'result': True, 'message': u"创建项目成功"})


@process_request
def get_all_project(request):
    """
    获取所有项目
    :param request:
    :return:
    """
    try:
        projects = Project.objects.get_all_project()
    except Exception as e:
        logger.error(u"获取项目失败", e)
        return render_json({'result': False, 'message': u"获取项目失败"})

    data = []
    for project in projects:
        data.append({
            'project_name': project.name,
            'project_introduction': project.introduction,
            'project_owner': project.owner,
            'project_participant': project.participant,
            'logo': project.logo
        })

    return render_json({'result': True, 'data': data})


@process_request
def search_project(request):
    """
    搜索项目
    :param request:
    :return:
    """
    pro_name = request.GET.get('pro_name', '')
    part_projects_res = Project.objects.get_user_part_project(request=request)
    owner_projects_res = Project.objects.get_user_owner_project(request=request)
    # 获取所用用户信息
    users = get_users(request)
    # 获取拥有的项目
    owner_project = []
    for project in owner_projects_res:
        if pro_name in project.name or pro_name == '':
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
        if pro_name in project.name or pro_name == '':
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


