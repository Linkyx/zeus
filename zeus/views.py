# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.contrib import auth


def index(request):
    user = request.session['name']
    return HttpResponse(user)

