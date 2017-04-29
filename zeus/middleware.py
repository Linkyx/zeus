# coding=utf-8

import sys
from django.http import HttpResponseRedirect


class Authentication(object):
    def __init__(self):
        pass

    def process_request(self, request):

        # 进行code授权时不需要校验用户登陆态
        if 'callback' in request.build_absolute_uri():
            return None

        try:
            user = request.session['id']
        # session中无user信息
        except KeyError:
            request.session['old_url'] = request.build_absolute_uri()
            return HttpResponseRedirect(
                # 'http://dev.adam.404befound.com/oauth/authorize?response_type=code&client_id=recruit&redirect_uri=http%3A%2F%2Frecruit.xiyoulinux.org%3A8000%2Fcallback')
                'https://sso.xiyoulinux.org/oauth/authorize?response_type=code&client_id=zeus&redirect_uri=http%3a%2f%2fwww.zeus.xiyoulinux.org%2fcallback&state=2&scope=all')

        return None
