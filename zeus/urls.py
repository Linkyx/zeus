# -*- coding:utf-8 -*-
"""zeus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .project_views import *
from .task_views import *
from .views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', index),


    # 项目接口
    url(r'^create_project/$', create_project),
    url(r'^get_all_project/$', get_all_project)
]
