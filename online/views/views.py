#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.http import JsonResponse
from django.urls import reverse
import json
from django import forms
from online.models import *
from .background import *

# Create your views here.

# 表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=50)
    password = forms.CharField(label='密　码', max_length=50, widget=forms.PasswordInput())

# Json的参数，用来转化date和decimal


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
            # try:
            #     if len(str(obj).split('.')[1]) <= 2:    # 说明是浮点型
            #         return thousands(float(obj))
            #     else:   # 说明是百分比
            #         return percents(float(obj))
            # except:
            #     return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)

# 登陆
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password_hash = hash_sha256(password)
            #获取的表单数据与数据库进行比较
            user = table_User.objects.filter(用户名__exact=username, 密码__exact=password_hash)
            if user:
                # 将username写入session
                request.session['username'] = username
                #比较成功，跳转至URL: overview
                response = HttpResponseRedirect(reverse('overview'))
                return response
            else:
                #比较失败，还在login
                Cnt = '用户名不存在，或密码输入错误<br/>'
                Cnt += '<a href="/online">继续登陆<a>'
                return HttpResponse(Cnt)
    else:
        uf = UserForm()
    return render(request, 'login.html', {'uf':uf})

# 注销
def logout(request):
    # 清空session
    request.session['username'] = ''
    #比较成功，跳转至登录页
    response = HttpResponseRedirect(reverse('login'))
    return response

# 首页
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = hash_sha256(uf.cleaned_data['password'])
            #添加到数据库
            table_User.objects.get_or_create(用户名=username, 密码=password)
            return HttpResponse('regist success!!')
    else:
        uf = UserForm()
    return render(request, 'home.html', {'uf':uf})
def home(request):
    username = request.COOKIES.get('username', '')
    permission = getPermission(username)
    if not permission.get('查看数据概览'):
        Cnt = '您没有权限登陆系统'
    else:
        Cnt = '你的权限为：{}'.format(permission)
    response = HttpResponse(Cnt)
    return response

# 登陆成功
def index(request):
    username = request.COOKIES.get('username','')
    return render_to_response('index.html', {'username':username})

# ajax
def ajax(request):
    return render(request, 'ajax.html')

from django.views.decorators.csrf import csrf_exempt
import decimal
@csrf_exempt
def ajax_test_add(request):
    a = decimal.Decimal(request.POST.get('a'))
    b = decimal.Decimal(request.POST.get('b'))
    s = float(a + b)
    return_json = {'result': s}
    return HttpResponse(json.dumps(return_json), content_type='application/json')
@csrf_exempt
def ajax_test_api_test(request):
    return_json = {'api_result': str(read_For_Company_GridDialog('WHERE 法定代表人=%s', ['姜民秀']))}
    return HttpResponse(json.dumps(return_json), content_type='application/json')

