# -*- coding:utf-8 -*-

from utils import logger, render_json
from models import Project


# 项目相关接口
def create_project(request):
    """
    创建项目
    :param request:
    :return:
    """
    name = 'test'
    introduction = 'dasasd'
    participant = 'dasdas'

    try:
        project = Project.objects.create_project(request=request, name=name, introduction=introduction, participant=participant)
    except Exception as e:
        logger.error(u"创建项目失败", e)

    return render_json({'result': True, 'message': u"创建项目成功"})


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
            'project_participant': project.participant
        })

    return render_json({'result': True, 'data': data})
