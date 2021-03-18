#-*-coding:utf-8 -*-
"""
@project:QSHOP
@File: manager_extras.py
@Time: 2019/12/4 20:44
@user：python-刘欢    
"""
from django import template

register =template.Library()

@register.filter()
def set_goods_name(obj):
    return  obj[:10]+'...'

@register.filter()
def set_password(obj):
    return  '*'*10




