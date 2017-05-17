# -*- coding:utf-8 -*-
from functools import wraps

import requests
from django.http import HttpResponseRedirect
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
        except Exception as e:
            return render(request, '500.html', {
                    'message': u'您无权进行该操作'
                })

    return returned_wrapper


def process_request(func):
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        # 进行code授权时不需要校验用户登陆态
        if 'callback' in request.build_absolute_uri():
            return func(request, *args, **kwargs)

        try:
            user = request.session['id']
        # session中无user信息
        except KeyError:
            request.session['old_url'] = request.build_absolute_uri()
            return HttpResponseRedirect(
                # 'http://dev.adam.404befound.com/oauth/authorize?response_type=code&client_id=recruit&redirect_uri=http%3A%2F%2Frecruit.xiyoulinux.org%3A8000%2Fcallback')
                'https://sso.xiyoulinux.org/oauth/authorize?response_type=code&client_id=zeus&redirect_uri=http%3a%2f%2fwww.zeus.xiyoulinux.org%2fcallback&state=2&scope=all')

        return func(request, *args, **kwargs)

    return returned_wrapper