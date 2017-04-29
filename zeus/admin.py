# -*- coding:utf-8 -*-
from django.contrib import admin
from models import Message, Project, Task


class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ['title', 'receiver']
    search_fields = ['title',]


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ['name',]


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name',]
    model = Task

admin.site.register(Message, MessageAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
