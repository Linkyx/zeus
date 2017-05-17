# -*- coding:utf-8 -*-
import time
from django.shortcuts import render

from utils import logger, render_json, get_users, get_all_users
from models import Project, Task
from decorators import user_has_project, process_request
from zeus.project_dynamic import create_dynamic


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
            img_path = os.path.join(os.path.dirname(__file__), 'static/images/app/', img_full_name)
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
                                                 participant=participant, logo='/static/images/app/' + img_full_name)
    except Exception as e:
        logger.error(u"创建项目失败", e)
        return render_json({'result': False, 'message': u"创建项目失败"})

    # 生成项目动态
    content = request.session['name'] + u"创建了项目"
    title = u"创建项目"
    create_dynamic(request=request, pid=project.pk,content=content, title=title)

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


@process_request
def get_project_user(request):
    """
    获取项目所有用户
    :param request:
    :return:
    """
    pid = request.GET.get('pid', '')
    try:
        project = Project.objects.get(pk=pid)
    except Exception as e:
        logger.error(u"获取项目用户列表失败", e)
        return render_json({'result': False})

    uids = project.participant.split(",")
    uids.append(project.owner)
    # 获取所有用户
    user_info = get_all_users(request)
    user_list = []
    # 过滤出当前项目下的用户
    for uid in uids:
        user = user_info[int(uid)]
        name = user['name']

    # for id, user in user_info.items():
        user_list.append({'id': uid, 'text': name})

    return render_json({'result': True, 'message': user_list})


@user_has_project
@process_request
def get_gantt_project(request, pid):
    """
    获取项目gantt图数据
    :param request:
    :return:
    """
    # 获取所有用户
    user_info = get_all_users(request)
    try:
        tasks = Task.objects.filter(project_id=pid).filter(status=0)
    except Exception as e:
        logger.error(u"获取项目甘特图失败", e)
        return render_json({"result": False})

    COLORS = ['ganttRed', "ganttGreen", "ganttBlue", "ganttOrange"]
    data = []

    for task in tasks:
        user_names = []
        for id in task.participant.split(','):
            user = user_info[int(id)]
            user_names.append(user['name'])
        begin = "/Date(" + str(int(time.mktime(task.begin_time.timetuple())*1000)) + ")/"
        finish = "/Date(" + str(int(time.mktime(task.finish_time.timetuple())*1000)) + ")/"
        data.append({
            'name': task.name,
            "desc": task.introduction,
            "values": [{
                "id": task.pk,
                "from": begin,
                "to": finish,
                "label": (",").join(user_names),
                "customClass": COLORS[task.pk % len(COLORS)]
            }]
        })
    if not data:
        empty = True
    else:
        empty = False
    return render_json({'result': True, 'data': data, 'empty': empty})


@process_request
def update_project_info(request):
    """
    更新项目信息
    :param request:
    :return:
    """
    name = request.POST.get('pro_name', '')
    introduction = request.POST.get('pro_intro', '')
    participant = request.POST.get('pro_part', '')
    img = request.FILES.get('pro_img', '')
    pid = request.POST.get('pid', '')
    # 获取项目当前信息
    try:
        project = Project.objects.filter(pk=pid)
    except Exception as e:
        logger.error(u"获取项目失败", e)
        return render_json({'result': False, 'message': u'获取项目失败'})

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
            img_path = os.path.join(os.path.dirname(__file__), 'static/images/app/', img_full_name)
            with open(img_path, 'wb') as f:
                for item in img.chunks():
                    f.write(item)
        except Exception as e:
            logger.error(u'图片写入失败', e)
            return render_json({'result': False, 'message': u'图片写入失败'})
    else:
        # 原先背景图
        img_path = project[0].logo.split('/')[-1]
        img_full_name = img_path
    try:
        project.update(name=name, introduction=introduction,
                       participant=participant, logo='/static/images/app/' + img_full_name)
    except Exception as e:
        logger.error(u"修改项目信息失败", e)
        return render_json({'result': False, 'message': u"修改项目信息失败"})

    # 生成项目动态
    content = request.session['name'] + u"修改了项目信息"
    title = u"项目信息修改"
    create_dynamic(request=request, pid=pid, content=content, title=title)

    return render_json({'result': True, 'message': u"项目信息修改成功"})


@process_request
def delete_project(request):
    """
    删除项目
    :param request:
    :return:
    """
    pid = request.POST.get('pid', '')

    try:
        project = Project.objects.filter(pk=pid).update(is_active=False)
    except Exception as e:
        logger.error(u"删除项目失败", e)
        return render_json({'result': False, 'message': u"删除项目失败"})

    # 将任务表中项目相关的任务标记为删除
    try:
        tasks = Task.objects.filter(project_id=pid).update(is_active=False)
    except Exception as e:
        logger.error(u"更改任务状态失败", e)
        return render_json({'result': False, 'message': u"删除项目失败"})

    return render_json({'result': True, 'message': u"删除项目成功"})