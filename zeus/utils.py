# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
import logging


# 封装写日志函数(待优化)
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

