#-*-coding:utf-8 -*-
"""
@project:QSHOP
@File: goods_extras.py
@Time: 2019/12/11 9:55
@user：python-刘欢    
"""
from django.template import Library

register = Library()

@register.filter('set_goods_number')
def set_goods_number(obj):
    return obj[:4]
