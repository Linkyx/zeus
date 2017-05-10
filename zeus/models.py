# -*- coding:utf-8 -*-
from django.db import models


class ProjectManager(models.Manager):
    """
    项目方发表
    """
    def get_queryset(self):
        return super(ProjectManager, self).get_queryset().filter(is_active=True)

    def create_project(self, request, name, introduction, participant, logo):
        """
        创建项目
        :return:
        """
        user = request.session['id']
        project = self.create(name=name, owner=user, participant=participant, introduction=introduction, logo=logo)

        return project

    def get_all_project(self):
        """
        获取所有项目
        :return:
        """
        projects = self.all()

        return projects

    def get_user_owner_project(self, request):
        """
        获取当前用户拥有的项目
        :return:
        """
        uid = request.session['id']

        # 获取用户拥有的项目
        projects = self.filter(owner=uid).order_by("-create_time")

        return projects

    def get_user_part_project(self, request):
        """
        获取当前用户参与的项目
        :return:
        """
        uid = str(request.session['id'])

        # 获取用户拥有的项目
        projects = self.all().order_by("-create_time")
        participant_projects = []
        for project in projects:
            uids = project.participant.split(',')
            if uid in uids:
                participant_projects.append(project)
        return participant_projects

    def is_project_user(self, request, pid):
        """
        判断用户是否拥有该项目的权限
        :return:
        """
        projects = self.filter(pk=pid)

        for project in projects:
            if str(request.session['id']) in project.owner.split(',') or \
                            str(request.session['id']) in project.participant.split(','):
                return True
            else:
                return False


class Project(models.Model):
    """
    项目表
    """
    name = models.CharField(u'项目名', max_length=255, blank=True, null=True)
    introduction = models.CharField(u'项目简介', max_length=255, blank=True, null=True)
    owner = models.CharField(u'项目拥有者', max_length=32, blank=True, null=True)
    participant = models.CharField(u'项目参与者', max_length=32, blank=True, null=True)
    is_active = models.BooleanField(u'是否未删除', default=True)
    logo = models.CharField(u'项目logo', blank=True, null=True, max_length=128)
    create_time = models.DateTimeField(u'创建时间', auto_now=True)
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
    def get_queryset(self):
        return super(TaskManager, self).get_queryset().filter(is_active=True)

    def create_task(self, request, name, introduction, participant, finish_time, begin_time, level, project_id):
        """
        创建任务
        :return:
        """
        owner = request.session['id']

        task = self.create(name=name, owner=owner, introduction=introduction, participant=participant, begin_time=begin_time,
                           finish_time=finish_time, level=level, project_id=project_id)

        return task

    def get_all_task(self):
        """
        获取所有任务
        :return:
        """
        tasks = self.all()

        return tasks

    def update_task_user(self, task_id, participant):
        """
        更新任务用户
        :return:
        """
        task = self.filter(pk=task_id)
        info = task.update(participant=participant)

        return info

    def get_task_pid_unfinish(self, pid):
        """
        根据项目id获取项目下待完成任务
        :return:
        """
        tasks = self.filter(project_id=pid, status=0).order_by('-level')

        return tasks

    def get_task_pid_finish(self, pid):
        """
        根据项目id获取项目下已完成任务
        :return:
        """
        tasks = self.filter(project_id=pid, status=2).order_by('-level')

        return tasks

    def delete_task(self, tid):
        """
        删除任务
        :param tid:
        :return:
        """
        task = self.filter(pk=tid).update(is_active=False)

        return task


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
    begin_time = models.DateTimeField(u'开始时间',  blank=True, null=True)
    finish_time = models.DateTimeField(u'完成时间',  blank=True, null=True)
    status = models.CharField(u'当前状态', choices=STATUS_CHOICES, default=0, max_length=16)
    level = models.CharField(u'任务级别', choices=LEVEL_CHOICES, default=0, max_length=16)
    is_active = models.BooleanField(u'是否未删除', default=True)
    project_id = models.CharField(u'项目id', max_length=32, blank=True, null=True, db_index = True)

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
    def get_queryset(self):
        return super(MessageManager, self).get_queryset().filter(is_active=True)


class Message(models.Model):
    """
    消息表
    """
    status = models.BooleanField(u'消息状态', default=False)
    title = models.CharField(u'消息标题', max_length=255, blank=True, null=True)
    content = models.CharField(u'消息内容', max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    sender = models.CharField(u'发送者', max_length=255, blank=True, null=True)
    receiver = models.CharField(u'接收者', max_length=255, blank=True, null=True)
    is_active = models.BooleanField(u'是否未删除', default=True)

    objects = MessageManager()

    class Meta:
        verbose_name = u'消息'
        verbose_name_plural = u'消息'

    def __unicode__(self):
        return self.title


class ProjectDynamicManager(models.Manager):
    """
    项目动态方发表
    """
    def create_dynamic(self, request, pid, content, title):
        """
        创建动态
        :return:
        """
        sender_id = request.session['id']
        dynamic = self.create(sender_id=sender_id, project_id=pid, content=content, title=title)

        return dynamic

    def get_all_dynamic(self):
        """
        获取动态
        :return:
        """
        return self.all()


class ProjectDynamic(models.Model):
    """
    项目动态
    """
    sender_id = models.CharField(u"动态创建者", max_length=32, blank=True, null=True)
    project_id = models.CharField(u"项目id", max_length=32, blank=True, null=True)
    content = models.CharField(u"内容", max_length=256, blank=True, null=True)
    title = models.CharField(u"标题", max_length=256, blank=True, null=True)
    create_time = models.DateTimeField(u'创建时间', auto_now=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    objects = ProjectDynamicManager()

    class Meta:
        verbose_name = u'项目动态'
        verbose_name_plural = u'项目动态'

    def __unicode__(self):
        return self.title
