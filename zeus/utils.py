# -*- coding: utf-8 -*-
import datetime
import time
from django.http import HttpResponse, HttpResponseRedirect
import json
import logging
import urllib2
import urllib


# 封装日志函数(待优化)
class logger_callback:
    def __init__(self):
        pass

    def info(self, message=''):
        logging.getLogger('info').info(message)

    def error(self, message='', e=''):
        logmessage = message + str(e)
        logging.getLogger('sourceDns.webdns.views').error(logmessage)

logger = logger_callback()


def render_json(dictionary={}):
    '''
    return the json string for response
    @summary: dictionary也可以是string, list数据
    @note:  返回结果是个dict, 请注意默认数据格式:
                                    {'result': '',
                                     'message':''
                                    }
    '''
    if type(dictionary) is not dict:
        # 如果参数不是dict,则组合成dict
        dictionary = {'result': True,
                      'message': dictionary,
                      }
    return HttpResponse(json.dumps(dictionary), content_type='application/json')


def get_all_users(request):
    """
    获取所有用户
    :param request:
    :return:
    """
    # 缓存所有用户信息， id name 头像
    try:
        header = {'Authorization': 'Bearer ' + request.session['token']}
        req = urllib2.Request(url='https://api.xiyoulinux.org/users?per_page=1000', headers=header)
        data = urllib2.urlopen(req)
        user_msg = json.loads(data.read())
    except Exception, e:
        return HttpResponseRedirect(request.session['old_url'])
    users = {}
    for item in user_msg['data']:
        user = {'name': item['name'], 'avatar': item['avatar_url']}
        users.update({item['id']: user})
    return users


def get_users(request):
    """
    获取除当前用户外所有用户
    :param request:
    :return:
    """
    # 缓存所有用户信息， id name 头像
    try:
        header = {'Authorization': 'Bearer ' + request.session['token']}
        req = urllib2.Request(url='https://api.xiyoulinux.org/users?per_page=1000', headers=header)
        data = urllib2.urlopen(req)
        user_msg = json.loads(data.read())
    except Exception, e:
        return HttpResponseRedirect(request.session['old_url'])
    users = {}
    for item in user_msg['data']:
        user = {'name': item['name'], 'avatar': item['avatar_url']}
        users.update({item['id']: user})
    users.pop(request.session['id'])
    return users


def refresh_user_session(request,user_msg):
    """
    更新session中用户信息
    :return:
    """
    request.session['avatar'] = user_msg['avatar_url']
    request.session['name'] = user_msg['name']
    request.session['id'] = user_msg['id']
    request.session['email'] = user_msg['email']
    request.session['phone'] = user_msg['phone']
    request.session['workplace'] = user_msg['workplace']
    request.session['job'] = user_msg['job']
    request.session['qq'] = user_msg['qq']
    request.session['wechat'] = user_msg['wechat']


def checkTime(starttime, endtime):
    """
    判断日期是否在某个范围内
    :param starttime:
    :param endtime:
    :return:
    """
    flag = False
    now = datetime.datetime.now()

    if now > starttime.replace(tzinfo=None) and now < endtime.replace(tzinfo=None):
        flag = True
    else:
        flag = False

    return flag


# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fG" % (G)
        else:
            return "%.2fM" % (M)
    else:
        return "%.2fkb" % (kb)
