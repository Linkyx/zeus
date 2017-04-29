# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User


def index(request):
    return HttpResponse('Welcome, <a target="_blank" href="/logout/">logout</a>')
