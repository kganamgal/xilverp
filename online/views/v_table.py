#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.http import JsonResponse
from django import forms
from online.models import *
# from .background import *
from .db_api import *

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# 表格实验
def ajax_table(request):
    return render(request, 'ajax_table.html')

@csrf_exempt
def ajax_table_company(request):
    try:
        clicked_id = int(request.POST.get('clicked_id'))    # 取得被点击的tree-item的id，即立项识别码
        assert clicked_id > 0
        # 取得该立项下全部后代节点
        grandchildern_ids = get_All_Grandchildren(clicked_id)
        t_rows = read_For_Payment_GridDialog('where 立项识别码 in %s', [grandchildern_ids + [clicked_id]])
    except:
        t_rows = read_For_Payment_GridDialog()
    t_head = uc.PaymentColLabels
    t_type = uc.PaymentColLabels_Type
    return_json = {'t_head': json.dumps(t_head, ensure_ascii=False, cls=CJsonEncoder),
                   't_type': json.dumps(t_type, ensure_ascii=False, cls=CJsonEncoder),
                   't_rows': json.dumps(t_rows, ensure_ascii=False, cls=CJsonEncoder),
    }
    return HttpResponse(json.dumps(return_json, ensure_ascii=False), content_type='application/json')


# 树实验
def test_tree(request):
    return render(request, 'test_tree.html')

@csrf_exempt
def ajax_jquery_tree(request):
    tree_datas = format_Details_By_Tree()
    return HttpResponse(json.dumps(tree_datas, ensure_ascii=False, cls=CJsonEncoder), content_type='application/json')

# bootstrap表格实验
def bt_test01(request):
    return render(request, 'bt_test01.html')

@csrf_exempt
def ajax_table_data(request):
    dict_Head = {
        '单位':     uc.CompanyColLabels,
        '立项':     uc.InitiationColLabels,
        '招标':     uc.BiddingColLabels,
        '合同':     uc.ContractColLabels,
        '分包合同': uc.SubContractColLabels,
        '变更':     uc.AlterationColLabels,
        '预算':     uc.BudgetColLabels,
        '付款':     uc.PaymentColLabels,
    }
    dict_Type = {
        '单位':     uc.CompanyColLabels_Type,
        '立项':     uc.InitiationColLabels_Type,
        '招标':     uc.BiddingColLabels_Type,
        '合同':     uc.ContractColLabels_Type,
        '分包合同': uc.SubContractColLabels_Type,
        '变更':     uc.AlterationColLabels_Type,
        '预算':     uc.BudgetColLabels_Type,
        '付款':     uc.PaymentColLabels_Type,
    }
    dict_API = {
        '单位':     read_For_Company_GridDialog,
        '立项':     read_For_Initiation_GridDialog,
        '招标':     read_For_Bidding_GridDialog,
        '合同':     read_For_Contract_GridDialog,
        '分包合同': read_For_SubContract_GridDialog,
        '变更':     read_For_Alteration_GridDialog,
        '预算':     read_For_Budget_GridDialog,
        '付款':     read_For_Payment_GridDialog,
    }
    key_table = request.POST.get('key_table')
    try:
        Init_UDID = int(request.POST.get('Init_UDID'))    # 取得被点击的tree-item的id，即立项识别码
        assert Init_UDID > 0
        # 取得该立项下全部后代节点
        if key_table == '预算':
            grandchildern_ids = get_All_Budget_Grandchildren_UDID(Init_UDID)
            t_rows = dict_API[key_table]('where 预算识别码 in %s', [grandchildern_ids + [Init_UDID]])
        else:
            grandchildern_ids = get_All_Grandchildren_UDID(Init_UDID)
            t_rows = dict_API[key_table]('where 立项识别码 in %s', [grandchildern_ids + [Init_UDID]])
    except:
        t_rows = dict_API[key_table]()
    t_head = dict_Head[key_table]
    t_type = dict_Type[key_table]
    return_json = {'t_head': json.dumps(t_head, ensure_ascii=False, cls=CJsonEncoder),
                   't_type': json.dumps(t_type, ensure_ascii=False, cls=CJsonEncoder),
                   't_rows': json.dumps(t_rows, ensure_ascii=False, cls=CJsonEncoder),
                  }
    return HttpResponse(json.dumps(return_json, ensure_ascii=False, cls=CJsonEncoder), content_type='application/json')

@csrf_exempt
def ajax_tree_data(request):
    dict_API = {
        '立项':     read_For_TreeList,
        '预算':     read_Budget_For_TreeList,
    }
    key_tree = request.POST.get('key_tree')
    return_json = dict_API[key_tree]()
    return HttpResponse(json.dumps(return_json, ensure_ascii=False, cls=CJsonEncoder), content_type='application/json')

@csrf_exempt
def ajax_treeTable(request):
    return_json = format_Details_By_Tree()
    return HttpResponse(json.dumps(return_json, ensure_ascii=False, cls=CJsonEncoder), content_type='application/json')