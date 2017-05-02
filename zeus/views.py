# -*- coding:utf-8 -*-

from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {

    })


def user_info(request):
    """
    用户信息页面
    :param request:
    :return:
    """
    return render(request, 'user_info.html', {

    })