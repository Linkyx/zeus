# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    user = request.session['name']
    return HttpResponse(user)


def home(request):
    return render(request, 'base.html', {})
