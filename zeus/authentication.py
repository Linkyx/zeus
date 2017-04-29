
# coding=utf-8

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.sessions.models import Session
import urllib2
import urllib
import json

GRANT_TYPE = 'authorization_code'
CLIENT_ID = 'zeus'
CLIENT_SECRET = '****************'
REDIRECT_URI = 'http://www.zeus.xiyoulinux.org/callback'


def callback(request):
    '''
    登陆校验,获取code进行并请求token
    :param request:
    :return:
    '''
    # 判断一下请求是否是来自授权服务器
    try:
        code = request.GET['code']
    except Exception, e:
        return Http404

    data = {
        'code': code,
        'grant_type': GRANT_TYPE,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }

    data = urllib.urlencode(data)

    f = urllib2.urlopen(
        url="https://sso.xiyoulinux.org/oauth/access_token",
        data=data)

    token = json.loads(f.read())['access_token']
    request.session['token'] = token

    try:
        header = {'Authorization': 'Bearer ' + token}
        req = urllib2.Request(url='https://api.xiyoulinux.org/me', headers=header)
        data = urllib2.urlopen(req)
        user_msg = json.loads(data.read())
    except Exception, e:
        return HttpResponseRedirect(request.session['old_url'])

    # 获取用户信息,存储在session中
    request.session['avatar'] = user_msg['avatar_url']
    request.session['name'] = user_msg['name']
    request.session['id'] = user_msg['id']
    # request.session['user'] = request.session['name']

    return HttpResponseRedirect(request.session['old_url'])


def logout(request):
    '''
    用户点击退出按钮
    :param request:
    :return:
    '''
    # 获取当前用户的session_id
    session_id = request.COOKIES.get('sessionid', '')

    # 清除当前已登录的session
    try:
        obj = Session.objects.get(pk=session_id)
        obj.delete()
    except Exception:
        pass

    return HttpResponseRedirect('http://sso.xiyoulinux.org/logout')

