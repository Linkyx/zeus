# -*- coding:utf-8 -*-
from django.db import models


class ProjectManager(models.Manager):
    """
    项目方发表
    """
    def get_query_set(self):
        return super(ProjectManager, self).get_query_set().filter(is_active=True)


class Project(models.Model):
    """
    项目表
    """
    name = models.CharField(u'项目名', max_length=255, blank=True, null=True)
    introduction = models.CharField(u'项目简介', max_length=255, blank=True, null=True)
    owner = models.CharField(u'项目拥有者', max_length=32, blank=True, null=True)
    participant = models.CharField(u'项目参与者', max_length=32, blank=True, null=True)
    is_active = models.BooleanField(u'是否未删除', default=True)
    objects = ProjectManager()

    class Meta:
        verbose_name = u'项目信息'
        verbose_name_plural = u'项目信息'

    def __unicode__(self):
        return self.name


class TaskManager(models.Manager):
    """
    任务方发表
    """
    def get_query_set(self):
        return super(TaskManager, self).get_query_set().filter(is_active=True)


class Task(models.Model):
    """
    任务表
    """
    STATUS_CHOICES = (
        (0, u'待处理'),
        (1, u'进行中'),
        (2, u'已完成')
    )

    LEVEL_CHOICES = (
        (0, u'低'),
        (1, u'中'),
        (2, u'高')
    )
    name = models.CharField(u'任务名', max_length=255, blank=True, null=True)
    introduction = models.CharField(u'任务简介', max_length=255, blank=True, null=True)
    owner = models.CharField(u'任务拥有者', max_length=32, blank=True, null=True)
    participant = models.CharField(u'任务参与者', max_length=32, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now=True)
    finish_time = models.DateTimeField(u'完成时间',  blank=True, null=True)
    status = models.CharField(u'当前状态', choices=STATUS_CHOICES, default=0, max_length=16)
    level = models.CharField(u'任务级别', choices=LEVEL_CHOICES, default=0, max_length=16)
    is_active = models.BooleanField(u'是否未删除', default=True)
    project = models.ForeignKey(Project)

    objects = TaskManager()

    class Meta:
        verbose_name = u'需求信息'
        verbose_name_plural = u'需求信息'

    def __unicode__(self):
        return self.name


class MessageManager(models.Manager):
    """
    消息方发表
    """
    def get_query_set(self):
        return super(MessageManager, self).get_query_set().filter(is_active=True)


class Message(models.Model):
    """
    消息表
    """
    status = models.BooleanField(u'消息状态', default=False)
    title = models.CharField(u'消息标题', max_length=255, blank=True, null=True)
    content = models.CharField(u'消息内容', max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    receiver = models.CharField(u'接收者', max_length=255, blank=True, null=True)
    is_active = models.BooleanField(u'是否未删除', default=True)

    objects = MessageManager()

    class Meta:
        verbose_name = u'消息信息'
        verbose_name_plural = u'消息信息'

    def __unicode__(self):
        return self.title



