# -*- coding:utf-8 -*-
from functools import wraps

from django.shortcuts import render

from models import Project


def user_has_project(func):
    """
    校验是否有当前项目权限
    """
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        try:
            pid = kwargs['pid']
            is_has = Project.objects.is_project_user(request=request, pid=pid)
            if is_has:
                return func(request, *args, **kwargs)
            else:
                return render(request, '500.html', {
                    'message': u'您无权进行该操作'
                })
        except Exception:
            return render(request, '500.html', {
                    'message': u'您无权进行该操作'
                })

    return returned_wrapper