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
from django.conf.urls import include, url, patterns
from django.contrib import admin
from .project_views import *
from .task_views import *
from .views import *
from .authentication import *


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += patterns('zeus.project_views',
                        # 项目接口
                        url(r'^create_project/$', 'create_project'),
                        url(r'^get_all_project/$', 'get_all_project')
                        )
urlpatterns += patterns('zeus.authentication',
                        # 登陆校验,获取code进行并请求token
                        url(r'^callback/$', 'callback'),
                        url(r'^logout/$', 'logout'),
                        )
urlpatterns += patterns('zeus.task_views',
                        # 任务接口
                        url(r'^create_task/$', 'create_task'),
                        url(r'^get_all_task/$', 'get_all_task'),
                        url(r'^update_task_user/$', 'update_task_user')
                        )

urlpatterns += patterns('zeus.views',
                        # 项目首页公共内容
                        url(r'^$', 'index'),
                        url(r'^home/$', 'home')
                        )
