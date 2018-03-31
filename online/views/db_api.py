#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-11-06 10:13:37
# @Last Modified by:   Administrator
# @Last Modified time: 2018-01-26 16:14:09

# thePD = pd.DataFrame(list(table_Initiation.objects.values('立项识别码',
# '父项立项识别码')))

# from collections import Iterable
# isinstance('abc',Iterable) # 判断目标是否可迭代


from django.db import connection
import online.userConst as uc
from online.models import *
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from django.db.models import Count, Min, Max, Sum
import pandas as pd
import numpy as np
import math
import hashlib
import base64
import hmac
import sys
import json
import decimal
import datetime
import time
import oss2

# 格式化字符串


def thousands(n): return '{:>,.2f}'.format(n)


def percents(n): return '{:>.2f}'.format((n or 0) * 100) + '%'

# HASH加密函数


def hash_sha256(string):
    '''
        Return a RSA string.
    '''
    m = hashlib.sha256()
    m.update(string.encode('utf8'))
    return m.hexdigest()

# 将对象转化为字典


def classToDict(obj):
    '''
        Transfer a object to a dictionary.
    '''
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__
    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
        return dict

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


def dictfetchall(cursor):
    '''
        Return all rows from a cursor as a dict
    '''
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# 树型数据


class treeModel:
    '''
        an node of a tree.
    '''

    def __init__(self, Id, value, fatherId, estimate, init_pay):
        self.Id = Id
        self.value = value
        self.fatherId = fatherId
        self.estimate = estimate
        self.init_pay = init_pay
        self.children = []
        self.children_pay = 0
        self.children_estimate = 0
        self.info = []

    def __str__(self):
        return '%d-%s' % (self.Id, self.value)

    def addChild(self, *child):
        self.children += child

    def getChildrenIds(self):
        '''
            get all children(son/daughter-like)'s Id by a list.
        '''
        result = []
        for child in self.children:
            result.append(child.Id)
        return result

    def getGrandChildrenCounts(self):
        '''
            get all grandchildren(grandson/grandgrandson-like)'s count by a list.
        '''
        global treeModel_recursion_childrenCounts_list_result
        treeModel_recursion_childrenCounts_list_result = []
        return self.recursion_childrenCounts()

    def recursion_childrenCounts(self):
        global treeModel_recursion_childrenCounts_list_result
        treeModel_recursion_childrenCounts_list_result.append(
            {'立项识别码': self.Id, '子项数量': len(self.children)})
        for child in self.children:
            child.recursion_childrenCounts()
        return treeModel_recursion_childrenCounts_list_result

    def getGrandChildrenIds(self, sortable=False):
        '''
            get all grandchildren(grandson/grandgrandson-like)'s Id by a list.
        '''
        global treeModel_recursion_childrenId_list_result
        treeModel_recursion_childrenId_list_result = []
        result = self.recursion_childrenId()
        result.remove(self.Id)
        sortable and result.sort()
        return result

    def recursion_childrenId(self):
        global treeModel_recursion_childrenId_list_result
        treeModel_recursion_childrenId_list_result.append(self.Id)
        for child in self.children:
            child.recursion_childrenId()
        return treeModel_recursion_childrenId_list_result

    def getGrandChildrenPayment(self):
        '''
            get all grandchildren(grandson/grandgrandson-like)'s Payment by a number.
        '''
        global treeModel_recursion_childrenPayment_list_result
        treeModel_recursion_childrenPayment_list_result = []
        return sum(self.recursion_childrenPayment())

    def recursion_childrenPayment(self):
        global treeModel_recursion_childrenPayment_list_result
        treeModel_recursion_childrenPayment_list_result.append(self.init_pay)
        for child in self.children:
            child.recursion_childrenPayment()
        return treeModel_recursion_childrenPayment_list_result

    def getEachChildrenInfo(self):
        '''
            get each grandchildren(grandson/grandgrandson-like)'s Info by a number.
        '''
        global treeModel_recursion_childrenInfo_list_result
        treeModel_recursion_childrenInfo_list_result = []
        return self.recursion_childrenInfo()

    def recursion_childrenInfo(self):
        global treeModel_recursion_childrenInfo_list_result
        for child in self.children:
            child.recursion_childrenInfo()
            self.children_pay += child.init_pay or 0 + child.children_pay or 0
            self.children_estimate += child.estimate or 0
        payed = self.children_pay or 0 + self.init_pay or 0
        treeModel_recursion_childrenInfo_list_result.append(
            {'立项识别码': self.Id, '概算已付款额': payed, '已分配概算':self.children_estimate, '子项数量': len(self.children)})
        return treeModel_recursion_childrenInfo_list_result

    def printTree(self, layer=0):
        print('  ' * layer + '%d-%s' % (self.Id, self.value))
        for child in self.children:
            child.printTree(layer + 1)


def read_For_InitTree(UDID=0):
    '''
        从立项表中读取数据，整理成treeModel数据结构，方便本地计算子项信息
    '''
    qs_Init = table_Initiation.objects.values(
        '立项识别码', '父项立项识别码', '项目名称', '分项名称', '项目概算')
    qs_Payment = table_Payment.objects.values(
        '立项识别码', '本次付款额')
    df_Init = pd.DataFrame(list(qs_Init)).fillna('')
    df_Payment = pd.DataFrame(list(qs_Payment)).fillna('')
    df_sumpay = df_Payment[['本次付款额']].groupby(
        df_Payment['立项识别码']).sum().reset_index()  # 按立项识别码聚合本次付款额
    df = pd.merge(df_Init, df_sumpay, on='立项识别码', how='left')
    js = df.to_dict('records')
    tm = {}
    tm[0] = treeModel(0, 'root', None, None, None)
    for item in js:
        Id, fatherId, value = int(item.get('立项识别码') or 0), int(
            item.get('父项立项识别码') or 0), item.get('分项名称') or item.get('项目名称')
        estimate = item.get('项目概算')
        init_pay = decimal.Decimal(0) if math.isnan(
            item.get('本次付款额')) else item.get('本次付款额')
        tm[Id] = treeModel(Id, value, fatherId, estimate, init_pay)
    for item in js:
        Id, fatherId = int(item.get('立项识别码') or 0), int(
            item.get('父项立项识别码') or 0)
        tm[fatherId or 0].addChild(tm[Id])
    return tm[UDID]


def base_read_For_InitTree(UDID=0):
    '''
        从立项表中读取数据，整理成treeModel数据结构，方便本地计算子项信息
    '''
    qs = table_Initiation.objects.values_list(
        '立项识别码', '父项立项识别码', '项目名称', '分项名称')
    tm = {}
    tm[0] = treeModel(0, 'root', None)
    for item in qs:
        Id, fatherId, value = item[0], item[1], item[3] or item[2]
        tm[Id] = treeModel(Id, value, fatherId)
    for item in qs:
        Id, fatherId = item[0], item[1]
        tm[fatherId or 0].addChild(tm[Id])
    return tm[UDID]


def format_Details_By_Tree():
    # 预自建过程
    sql1 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_UDID_table (立项识别码 INT);
        '''
    sql2 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_pay_table (立项识别码 INT, 已分配概算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql3 = '''
        TRUNCATE TABLE tmp_UDID_table;
        '''
    sql4 = '''
        TRUNCATE TABLE tmp_pay_table;
        '''
    # 将自身的立项识别码及全部子项的立项识别码导入表tmp_UDID_table
    sql5 = '''
        DROP PROCEDURE IF EXISTS get_all_children;
        '''
    sql6 = '''
        CREATE PROCEDURE `get_all_children` (areaId INT)
        BEGIN
            DECLARE sTemp VARCHAR(4000);
            DECLARE sTempChd VARCHAR(4000);
            SET sTemp = '$';
            SET sTempChd = cast(areaId as char);
            INSERT INTO tmp_UDID_table (立项识别码) VALUES(areaId);
            WHILE sTempChd is not NULL DO
                SET sTemp = CONCAT(sTemp,',',sTempChd);
                INSERT INTO tmp_UDID_table (立项识别码) SELECT 立项识别码 FROM tabel_立项信息 WHERE FIND_IN_SET(父项立项识别码,sTempChd)>0;
                SELECT group_concat(立项识别码) INTO sTempChd FROM tabel_立项信息 WHERE FIND_IN_SET(父项立项识别码,sTempChd)>0;
            END WHILE;
        END;
    '''
    # 遍历立项信息表，将立项识别码-项下已付款存入临时表tmp_pay_table
    sql7 = '''
        drop procedure if exists proc_tmp;
        '''
    sql8 = '''
        create procedure `proc_tmp`()
        BEGIN
            declare done int default 0;
            declare UDID bigint;
            declare idCur cursor for select 立项识别码 from tabel_立项信息 ORDER BY 立项识别码;
            declare continue handler for not FOUND set done = 1;
            open idCur;
            REPEAT
                fetch idCur into UDID;
                if not done THEN
                    TRUNCATE TABLE tmp_UDID_table;
                    CALL get_all_children(UDID);
                    INSERT INTO tmp_pay_table (立项识别码, 已分配概算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(项目概算) FROM tabel_立项信息 WHERE 父项立项识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 立项识别码 IN (SELECT 立项识别码 FROM tmp_UDID_table));
                end if;
            until done end repeat;
            close idCur;
        END;
        '''
    sql9 = '''
        CALL proc_tmp();
    '''
    # 正式
    sql10 = '''SELECT           I.立项识别码 AS 立项识别码, ifnull(分项名称, 项目名称) AS 项目名称, 合同名称, 项目概算,
                                  已分配概算/项目概算 AS 概算已分配率, T.已付款/项目概算 AS 概算付款比,
                                  招标方式, 中标价, 合同值_最新值 AS 合同值, P.已付款/合同值_最新值 AS 合同付款比, T.已付款, 分包合同数量
                 FROM             (SELECT * FROM tabel_立项信息 ORDER BY 立项识别码) AS I
                       LEFT JOIN  tabel_招标信息 AS B ON I.立项识别码=B.立项识别码
                       LEFT JOIN  tabel_合同信息 AS C ON I.立项识别码=C.立项识别码
                       LEFT JOIN  (SELECT 立项识别码, COUNT(*) AS 分包合同数量 FROM tabel_分包合同信息 GROUP BY 立项识别码) AS D ON I.立项识别码=D.立项识别码
                       LEFT JOIN  (SELECT 立项识别码, SUM(本次付款额) AS 已付款 FROM tabel_付款信息 GROUP BY 立项识别码) AS P ON I.立项识别码=P.立项识别码
                       LEFT JOIN  tmp_pay_table AS T ON I.立项识别码=T.立项识别码
           '''
    sql11 = '''SELECT 立项识别码, 父项立项识别码 FROM tabel_立项信息'''
    with connection.cursor() as cursor:
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        cursor.execute(sql5)
        cursor.execute(sql6)
        cursor.execute(sql7)
        cursor.execute(sql8)
        cursor.execute(sql9)
        cursor.execute(sql10)
        data = dictfetchall(cursor)
        cursor.execute(sql11)
        hierarchy = list(map(list, cursor.fetchall()))
    # 将列表形式的数据格式化成字典型的
    dict_data = {}
    for da in data:
        key = da.pop('立项识别码')
        dict_data[key] = da
    # 将层级数据结构转化为dataframe
    array_hierarchy = np.array(hierarchy)
    frame_hierarchy = pd.DataFrame(
        array_hierarchy, columns=['立项识别码', '父项立项识别码'])

    def get_All_Roots():
        frame = frame_hierarchy[frame_hierarchy['父项立项识别码'].isnull()]
        list_frame = frame['立项识别码'].values.tolist()
        return [[x, 0] for x in list_frame]

    def get_All_Children(UDID, deep=0):    # 只获取子代，不获得更深后代
        frame = frame_hierarchy[frame_hierarchy['父项立项识别码'] == UDID]
        list_frame = frame['立项识别码'].values.tolist()
        return [[x, deep + 1] for x in list_frame]
    # 开始迭代获取数据层级
    roots_info = get_All_Roots()
    # 访问这些根节点，取得每个根节点的所有子项，存入其中

    def fix_treeTable_datas(roots_info):
        # 取得逻辑骨架，再将细节附着在骨架上
        i = 0
        while i < len(roots_info):
            UDID = roots_info[i][0]
            deep = roots_info[i][1]
            children = get_All_Children(UDID, deep)
            if children:
                prefix = roots_info[:(i + 1)]
                suffix = roots_info[(i + 1):]
                roots_info = prefix + children + suffix
            i += 1
        for i in range(len(roots_info)):
            Id, Level = roots_info[i]
            roots_info[i] = {'立项识别码': Id, '层级': Level}
            roots_info[i].update(dict_data.get(Id))
        return roots_info
    return fix_treeTable_datas(roots_info)


def read_For_TreeList():
    # 正式
    sql = '''SELECT 立项识别码 AS Id, ifnull(分项名称, 项目名称) AS name, 父项立项识别码 AS PId
               FROM tabel_立项信息
           ORDER BY 立项识别码
          '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)


def new_read_For_TreeList():
    # 正式
    sql = '''SELECT 立项识别码 AS Id, ifnull(分项名称, 项目名称) AS name, 父项立项识别码 AS PId
               FROM tabel_立项信息
           ORDER BY 立项识别码
          '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)

# 单位管理


def read_For_Company_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = 'SELECT {} FROM tabel_单位信息 '.format(
        ', '.join(uc.CompanyColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)
        # return [list(x) for x in cursor.fetchall()]


def old_save_For_Company_GridDialog(**data):
    '''
        This function can insert/update data for table_Company.
        input data({'单位识别码': 1, '单位名称': '青岛X公司', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    # 参数合法性校验
    if not data:
        return '您未输入任何数据'
    # 参数数量校验
    if len(data) != len(uc.CompanyFields):
        return '参数数量(%d)错误，应为(%d)个' % (len(data), len(uc.CompanyFields))
    # 确保UDID是整数
    try:
        UDID = int(data.get('单位识别码') or 0)
    except Exception as e:
        return str(e)
    # 确保传入的参数类型正确
    dict_type = dict(zip(uc.CompanyFields, uc.CompanyFields_Type))
    for field, value in data.items():
        if field not in uc.CompanyFields:
            return '无法存储<%s>，请重新输入' % field
        _type = dict_type.get(field)
        if (_type == '整数型' and not (type(value) == type(1) or value is None))\
                or (_type == '浮点型' and not (type(value) == type(1.0) or type(value) == type(decimal.Decimal(1.0)) or type(value) == type(1) or value is None))\
                or (_type == '字符串型' and not (type(value) == type('abc') or value is None))\
                or (_type == '文本型' and not (type(value) == type('abc') or value is None)):
            return '<%s:%s>类型(%s)错误，应为<%s>，请检查' % (field, str(value), str(type(value)), _type)
        if _type == '日期型':
            try:
                data[field] = datetime.date(
                    *list(time.strptime(data.get(field), "%Y-%m-%d"))[:3])
            except Exception as e:
                return str(e)
    # 判断应该用insert还是update
    try:
        if UDID > 0:    # UDID存在，说明应该update
            # 确保该项存在
            flag = not table_Company.objects.filter(单位识别码=UDID)
            if flag:
                return '单位识别码为<%d>的记录尚不存在，无法修改，请检查' % UDID
            # 数据合法性校验（是否存在重码）
            flag = table_Company.objects.filter(
                单位名称__exact=data.get('单位名称')).exclude(单位识别码=UDID)
            if flag:
                return '<%s>已存在，请检查' % data.get('单位名称')
            flag = table_Company.objects.filter(
                单位识别码__exact=UDID).update(**data)
            if flag:
                return 'Done'
        else:           # UDID不存在，说明应该insert
            # 数据合法性校验（是否存在重码）
            flag = table_Company.objects.filter(单位名称__exact=data.get('单位名称'))
            if flag:
                return '<%s>已存在，请检查' % data.get('单位名称')
            # 数据合法性校验（是否未输入单位名称）
            flag = not data.get('单位名称')
            if flag:
                return '<单位名称>未填写，请检查'
            flag = table_Company.objects.create(**data)
            if flag:
                return 'Done'
    except Exception as e:
        return str(e)

# 立项管理


def read_For_Initiation_GridDialog(where_sql='', where_list=[], order_sql='ORDER BY 立项识别码', order_list=[]):
    # 预自建过程
    sql1 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_UDID_table (立项识别码 INT);
        '''
    sql2 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_pay_table (立项识别码 INT, 已分配概算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql2_5 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_parent_pay_table (立项识别码 INT, 已分配概算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql3 = '''
        TRUNCATE TABLE tmp_UDID_table;
        '''
    sql4 = '''
        TRUNCATE TABLE tmp_pay_table;
        '''
    sql4_5 = '''
        TRUNCATE TABLE tmp_parent_pay_table;
        '''
    # 将自身的立项识别码及全部子项的立项识别码导入表tmp_UDID_table
    sql5 = '''
        DROP PROCEDURE IF EXISTS get_all_children;
        '''
    sql6 = '''
        CREATE PROCEDURE `get_all_children` (areaId INT)
        BEGIN
            DECLARE sTemp VARCHAR(4000);
            DECLARE sTempChd VARCHAR(4000);
            SET sTemp = '$';
            SET sTempChd = cast(areaId as char);
            INSERT INTO tmp_UDID_table (立项识别码) VALUES(areaId);
            WHILE sTempChd is not NULL DO
                SET sTemp = CONCAT(sTemp,',',sTempChd);
                INSERT INTO tmp_UDID_table (立项识别码) SELECT 立项识别码 FROM tabel_立项信息 WHERE FIND_IN_SET(父项立项识别码,sTempChd)>0;
                SELECT group_concat(立项识别码) INTO sTempChd FROM tabel_立项信息 WHERE FIND_IN_SET(父项立项识别码,sTempChd)>0;
            END WHILE;
        END;
    '''
    # 遍历立项信息表，将立项识别码-项下已付款存入临时表tmp_pay_table
    sql7 = '''
        drop procedure if exists proc_tmp;
        '''
    sql8 = '''
        create procedure `proc_tmp`()
        BEGIN
            declare done int default 0;
            declare UDID bigint;
            declare idCur cursor for select 立项识别码 from tabel_立项信息 ORDER BY 立项识别码;
            declare continue handler for not FOUND set done = 1;
            open idCur;
            REPEAT
                fetch idCur into UDID;
                if not done THEN
                    TRUNCATE TABLE tmp_UDID_table;
                    CALL get_all_children(UDID);
                    INSERT INTO tmp_pay_table (立项识别码, 已分配概算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(项目概算) FROM tabel_立项信息 WHERE 父项立项识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 立项识别码 IN (SELECT 立项识别码 FROM tmp_UDID_table));
                    INSERT INTO tmp_parent_pay_table (立项识别码, 已分配概算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(项目概算) FROM tabel_立项信息 WHERE 父项立项识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 立项识别码 IN (SELECT 立项识别码 FROM tmp_UDID_table));
                end if;
            until done end repeat;
            close idCur;
        END;
        '''
    sql9 = '''
        CALL proc_tmp();
    '''
    # 正式
    # 编辑/etc/my.cnf文件，加入如下参数，重启mysql
    # sql_mode = "STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER"
    sql = '''SELECT {} FROM
             (SELECT           A.立项识别码, A.项目名称, A.分项名称, A.父项立项识别码, B.项目名称 AS 父项项目名称,
                               B.分项名称 AS 父项分项名称, 子项数量,
                               B.项目概算 AS 父项项目概算,
                               ifnull(B.项目概算, 0)-ifnull(TP.已分配概算, 0)+ifnull(A.项目概算, 0) AS 项目概算上限,
                               A.建设单位识别码, U1.单位名称 AS 建设单位名称, A.代建单位识别码, U2.单位名称 AS 代建单位名称,
                               A.立项文件名称, A.立项简介, A.立项时间, A.项目概算, T.已分配概算, A.项目概算-T.已分配概算 AS 未分配概算,
                               T.已分配概算/A.项目概算 AS 概算分配比, T.已付款 AS 概算已付款额, A.项目概算-T.已付款 AS 概算可付余额,
                               T.已付款/A.项目概算 AS 概算付款比, A.立项备注
              FROM             tabel_立项信息 AS A
                   LEFT JOIN   tabel_立项信息 AS B  ON A.父项立项识别码=B.立项识别码
                   LEFT JOIN   (SELECT 父项立项识别码, COUNT(*) AS 子项数量 FROM tabel_立项信息 GROUP BY 父项立项识别码) AS C ON A.立项识别码=C.父项立项识别码
                   LEFT JOIN   tabel_单位信息 AS U1 ON A.建设单位识别码=U1.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U2 ON A.代建单位识别码=U2.单位识别码
                   LEFT JOIN   tmp_pay_table AS T ON A.立项识别码=T.立项识别码
                   LEFT JOIN   tmp_parent_pay_table AS TP ON A.父项立项识别码=TP.立项识别码
             ) AS Origin
          '''.format(', '.join(uc.InitiationColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql1)
    with connection.cursor() as cursor:
        cursor.execute(sql2)
    with connection.cursor() as cursor:
        cursor.execute(sql2_5)
    with connection.cursor() as cursor:
        cursor.execute(sql3)
    with connection.cursor() as cursor:
        cursor.execute(sql4)
    with connection.cursor() as cursor:
        cursor.execute(sql4_5)
    with connection.cursor() as cursor:
        cursor.execute(sql5)
    with connection.cursor() as cursor:
        cursor.execute(sql6)
    with connection.cursor() as cursor:
        cursor.execute(sql7)
    with connection.cursor() as cursor:
        cursor.execute(sql8)
    with connection.cursor() as cursor:
        cursor.execute(sql9)
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)


def new_read_For_Initiation_GridDialog(column_name='', comparison=None, operator='='):
    '''
        使用pandas来分析orm得来的数据库原始记录，得到前端需要的数据
        func('立项识别码', 42)
        func('立项识别码', [43, 44], 'in')
    '''
    # 从数据库读取原始信息
    qs_Init = table_Initiation.objects.values()
    qs_Company = table_Company.objects.values()
    qs_Payment = table_Payment.objects.values()
    parent_child_tree = read_For_InitTree().getEachChildrenInfo()  # 生成立项数据的父子树
    # 将原始信息转化成dataframe格式
    df_Init = pd.DataFrame(list(qs_Init)).fillna('')
    df_Company = pd.DataFrame(list(qs_Company)).fillna('')
    df_Payment = pd.DataFrame(list(qs_Payment)).fillna('')
    df_parent_child_tree = pd.DataFrame(parent_child_tree).fillna('')
    # 开始连接各表
    df = pd.merge(df_Init, df_Init[['立项识别码', '项目名称', '分项名称', '项目概算']],
                  left_on='父项立项识别码', right_on='立项识别码', suffixes=('',  '_Parent'), how='left')
    df['父项项目名称'] = df['项目名称_Parent']
    df['父项分项名称'] = df['分项名称_Parent']
    df['父项项目概算'] = df['项目概算_Parent']
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='建设单位识别码', right_on='单位识别码', how='left')
    df['建设单位名称'] = df['单位名称']
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='代建单位识别码', right_on='单位识别码', suffixes=('', '_1'), how='left')
    df['代建单位名称'] = df['单位名称_1']
    df = pd.merge(df, df_parent_child_tree,
                  on='立项识别码', suffixes=('', '_2'), how='left')
    df = pd.merge(df, df_parent_child_tree,
                  left_on='父项立项识别码', right_on='立项识别码', suffixes=('', '_3'), how='left')
    # 筛选需要显示的字段
    df['概算可付余额'] = df['项目概算'] - df['概算已付款额']
    df['父项已分配概算'] = df['已分配概算_3']
    df['项目概算上限'] = df['父项项目概算'] - df['父项已分配概算'] + df['项目概算']

    def flag(x1, x2):
        if not x1:
            return 0
        elif x2:
            return float(x1) / float(x2)
        else:
            return None
    df['未分配概算'] = df['项目概算'] - df['已分配概算']
    df['概算付款比'] = pd.DataFrame(list(map(flag, df['概算已付款额'], df['项目概算'])))
    df['概算分配比'] = pd.DataFrame(list(map(flag, df['已分配概算'], df['项目概算'])))
    result = df[uc.InitiationColLabels].fillna('')

    if column_name and operator == '=':
        result = result[result[column_name] == comparison]
    elif column_name and operator == 'in':
        result = result[result[column_name].isin(comparison)]
    result = result.to_dict('records')
    result = sorted(result, key=lambda x: x.get('立项识别码'), reverse=False)
    return result


def old_save_For_Initiation_GridDialog(**data):
    '''
        This function can insert/update data for table_Initiation.
        input data({'立项识别码': 1, '项目名称': '北王安置房', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    # 参数合法性校验
    if not data:
        return '您未输入任何数据'
    # 参数数量校验
    if len(data) != len(uc.InitiationFields):
        return '参数数量(%d)错误，应为(%d)个' % (len(data), len(uc.InitiationFields))
    # 确保UDID是整数
    try:
        UDID = int(data.get('立项识别码') or 0)
    except Exception as e:
        return str(e)
    # 确保传入的参数类型正确
    dict_type = dict(zip(uc.InitiationFields, uc.InitiationFields_Type))
    for field, value in data.items():
        if field not in uc.InitiationFields:
            return '无法存储<%s>，请重新输入' % field
        _type = dict_type.get(field)
        if (_type == '整数型' and not (type(value) == type(1) or value is None))\
                or (_type == '浮点型' and not (type(value) == type(1.0) or type(value) == type(1) or type(value) == type(decimal.Decimal(1.0)) or value is None))\
                or (_type == '字符串型' and not (type(value) == type('abc') or value is None))\
                or (_type == '文本型' and not (type(value) == type('abc') or value is None)):
            return '<%s:%s>类型(%s)错误，应为<%s>，请检查' % (field, str(value), str(type(value)), _type)
        elif _type == '日期型':
            try:
                data[field] = datetime.date(
                    *list(time.strptime(data.get(field), "%Y-%m-%d"))[:3])
            except Exception as e:
                return str(e)
    # 判断应该用insert还是update
    try:
        # 项目名称不应为空
        if not data.get('项目名称'):
            return '请输入<%s>字段' % '项目名称'
        # 如果有父项，项目名称应与父项项目名称一致
        parentUDID = data.get('父项立项识别码') or 0
        if parentUDID:
            project = data.get('项目名称')
            orm_init = table_Initiation.objects.filter(
                立项识别码=parentUDID).values()
            if orm_init:
                parent_project = orm_init[0].get('项目名称') or ''
                flag = project != parent_project
                if flag:
                    return '<项目名称>(%s)与<父项项目名称>(%s)不一致，请修改' % (project, parent_project)
        # 父项应为空，或父项的父项...应为空，否则说明有循环引用象
        for i in range(20):
            if not parentUDID:
                break
            orm_init = table_Initiation.objects.filter(
                立项识别码=parentUDID).values()
            if orm_init:
                parentUDID = orm_init[0].get('父项立项识别码')
            else:
                break
        else:
            return '该项深度超过20层或存在循环引用现象，请优化项目结构'
        # update
        if UDID > 0:
            # 确保该项存在
            flag = not table_Initiation.objects.filter(立项识别码=UDID)
            if flag:
                return '立项识别码为<%d>的记录尚不存在，无法修改，请检查' % UDID
            # 项目名称、分项名称不应有重复
            flag = table_Initiation.objects.filter(项目名称__exact=data.get(
                '项目名称'), 分项名称__exact=data.get('分项名称')).exclude(立项识别码=UDID)
            if flag:
                return '<%s-%s>已存在，请检查' % (data.get('项目名称'), (data.get('分项名称') or ''))
            # 查询一次数据库
            old_data = read_For_Initiation_GridDialog(
                'WHERE 立项识别码=%s', [UDID])[0]
            # 项目概算应>=已付款
            estimate = float(data.get('项目概算') or 0)
            payed_estimate = float(old_data.get('概算已付款额') or 0)
            if estimate < payed_estimate:
                return '<项目概算>(%f)过低，请调整为不低于<概算已付款额>(%f)' % (estimate, payed_estimate)
            # 项目概算应>=已分配概算
            estimate = float(data.get('项目概算') or 0)
            distributed_estimate = float(old_data.get('已分配概算') or 0)
            if estimate < distributed_estimate:
                return '<项目概算>(%f)过低，请调整为不低于<已分配概算>(%f)' % (estimate, distributed_estimate)
            # 父项存在时，项目概算应<= 项目概算上限
            parentUDID = data.get('父项立项识别码') or 0
            estimate = float(data.get('项目概算') or 0)
            old_estimate = float(old_data.get('项目概算') or 0)
            parent_data = read_For_Initiation_GridDialog(
                'WHERE 立项识别码=%s', [UDID])
            if parent_data:
                parent_estimate = float(parent_data[0].get('项目概算') or 0)
                parent_distributed_estimate = float(
                    parent_data[0].get('已分配概算') or 0)
                limit_estimate = float(
                    parent_estimate - parent_distributed_estimate + old_estimate)
                if estimate > limit_estimate:
                    return '<项目概算>(%f)过高，请调整为不高于(%f)' % (estimate, limit_estimate)
            # 正戏
            flag = table_Initiation.objects.filter(
                立项识别码__exact=UDID).update(**data)
            if flag:
                return 'Done'
        # insert
        else:
            # 确保项目名称、项目分项不重复
            flag = table_Initiation.objects.filter(
                项目名称__exact=data.get('项目名称'), 分项名称__exact=data.get('分项名称'))
            if flag:
                return '<%s-%s>已存在，请检查' % (data.get('项目名称'), (data.get('分项名称') or ''))
            # 父项存在时，项目概算应<= 父项概算-父项已分配概算
            parentUDID = data.get('父项立项识别码') or 0
            estimate = float(data.get('项目概算') or 0)
            parent_data = read_For_Initiation_GridDialog(
                'WHERE 立项识别码=%s', [UDID])
            if parent_data:
                parent_estimate = float(parent_data[0].get('项目概算') or 0)
                parent_distributed_estimate = float(
                    parent_data[0].get('已分配概算') or 0)
                limit_estimate = float(
                    parent_estimate - parent_distributed_estimate)
                if estimate > limit_estimate:
                    return '<项目概算>(%f)过高，请调整为不高于(%f)' % (estimate, limit_estimate)
            # 正戏
            flag = table_Initiation.objects.create(**data)
            if flag:
                return 'Done'
    except Exception as e:
        return str(e)


def get_All_Grandchildren(UDID):
    '''
        取得某项下全部子项、孙项等的立项识别码
    '''
    sql1 = '''
    	  set global log_bin_trust_function_creators=1;
          DROP FUNCTION IF EXISTS queryChildrenAreaInfo;
          '''
    sql2 = '''
          CREATE FUNCTION `queryChildrenAreaInfo` (areaId INT)
          RETURNS VARCHAR(4000)
          BEGIN
              DECLARE sTemp VARCHAR(4000);
              DECLARE sTempChd VARCHAR(4000);
              SET sTemp = '$';
              SET sTempChd = cast(areaId as char);
              WHILE sTempChd is not NULL DO
                  SET sTemp = CONCAT(sTemp,',',sTempChd);
                  SELECT group_concat(立项识别码) INTO sTempChd FROM tabel_立项信息 where FIND_IN_SET(父项立项识别码,sTempChd)>0;
              END WHILE;
              return sTemp;
          END;
          '''
    sql = '''SELECT queryChildrenAreaInfo(%s);'''
    sql_list = [UDID]
    with connection.cursor() as cursor:
        cursor.execute(sql1)
        cursor.execute(sql2)
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        fetchall = cursor.fetchall()[0][0].split(',')[2:]
        return dictfetchall(cursor)

# 招标管理


def read_For_Bidding_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
                 (SELECT           招标识别码, A.立项识别码 AS 立项识别码, 项目名称, 分项名称,
                                   建设单位识别码, U4.单位名称 AS 建设单位名称, 代建单位识别码, U5.单位名称 AS 代建单位名称,
                                   招标方式, 招标单位识别码,
                                   U1.单位名称 AS 招标单位名称, 招标代理识别码, U2.单位名称 AS 招标代理单位名称, 招标简介, 投标单位, 项目概算,
                                   预算控制价, 招标文件定稿时间, 公告邀请函发出时间, 开标时间, 中标通知书发出时间,
                                   中标单位识别码, U3.单位名称 AS 中标单位名称, 中标价, 招标备注
                  FROM             tabel_招标信息 AS A
                       LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                       LEFT JOIN   tabel_单位信息 AS U1 ON A.招标单位识别码=U1.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U2 ON A.招标代理识别码=U2.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U3 ON A.中标单位识别码=U3.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U4 ON I.建设单位识别码=U4.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U5 ON I.代建单位识别码=U5.单位识别码
                 ) AS Origin
          '''.format(', '.join(uc.BiddingColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)


def new_read_For_Bidding_GridDialog(column_name='', comparison=None, operator='='):
    qs_Init = table_Initiation.objects.values()
    qs_Bidding = table_Bidding.objects.values()
    qs_Company = table_Company.objects.values()
    df_Init = pd.DataFrame(list(qs_Init)).fillna('')
    df_Bidding = pd.DataFrame(list(qs_Bidding)).fillna('')
    df_Company = pd.DataFrame(list(qs_Company)).fillna('')
    df = pd.merge(df_Bidding, df_Init, on='立项识别码', how='left')
    df = pd.merge(df, df_Company, left_on='建设单位识别码',
                  right_on='单位识别码', suffixes=('',  '1'), how='left')
    df['建设单位识别码'] = df['单位识别码']
    df['建设单位名称'] = df['单位名称']
    df = pd.merge(df, df_Company, left_on='代建单位识别码',
                  right_on='单位识别码', suffixes=('',  '2'), how='left')
    df['代建单位识别码'] = df['单位识别码']
    df['代建单位名称'] = df['单位名称']
    df = pd.merge(df, df_Company, left_on='招标单位识别码',
                  right_on='单位识别码', suffixes=('',  '3'), how='left')
    df['招标单位识别码'] = df['单位识别码']
    df['招标单位名称'] = df['单位名称']
    df = pd.merge(df, df_Company, left_on='招标代理识别码',
                  right_on='单位识别码', suffixes=('',  '4'), how='left')
    df['招标代理识别码'] = df['单位识别码']
    df['招标代理单位名称'] = df['单位名称']
    df = pd.merge(df, df_Company, left_on='中标单位识别码',
                  right_on='单位识别码', suffixes=('',  '5'), how='left')
    df['中标单位识别码'] = df['单位识别码']
    df['中标单位名称'] = df['单位名称']
    result = df[uc.BiddingColLabels].fillna('')
    if column_name and operator == '=':
        result = result[result[column_name] == comparison]
    elif column_name and operator == 'in':
        result = result[result[column_name].isin(comparison)]
    result = result.to_dict('records')
    result = sorted(result, key=lambda x: x.get('招标识别码'), reverse=False)
    return result


def old_save_For_Bidding_GridDialog(**data):
    '''
        This function can insert/update data for table_Bidding.
        input data({'招标识别码': 1, '招标方式': '公开招标', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    # 参数合法性校验
    if not data:
        return '您未输入任何数据'
    # 参数数量校验
    if len(data) != len(uc.BiddingFields):
        return '参数数量(%d)错误，应为(%d)个' % (len(data), len(uc.BiddingFields))
    # 确保UDID是整数
    try:
        UDID = int(data.get('招标识别码') or 0)
    except Exception as e:
        return str(e)
    # 确保传入的参数类型正确
    dict_type = dict(zip(uc.BiddingFields, uc.BiddingFields_Type))
    for field, value in data.items():
        if field not in uc.BiddingFields:
            return '无法存储<%s>，请重新输入' % field
        _type = dict_type.get(field)
        if (_type == '整数型' and not (type(value) == type(1) or value is None))\
                or (_type == '浮点型' and not (type(value) == type(1.0) or type(value) == type(1) or type(value) == type(decimal.Decimal(1.0)) or value is None))\
                or (_type == '字符串型' and not (type(value) == type('abc') or value is None))\
                or (_type == '文本型' and not (type(value) == type('abc') or value is None)):
            return '<%s:%s>类型(%s)错误，应为<%s>，请检查' % (field, str(value), str(type(value)), _type)
        elif _type == '日期型':
            try:
                data[field] = datetime.date(
                    *list(time.strptime(data.get(field), "%Y-%m-%d"))[:3])
            except Exception as e:
                return str(e)
    # 判断应该用insert还是update
    try:
        # 立项识别码必须存在、对应的立项必须存在
        InitUDID = data.get('立项识别码') or 0
        Init_data = read_For_Initiation_GridDialog(
            'WHERE 立项识别码=%s', [InitUDID])
        flag = not (InitUDID and Init_data)
        if flag:
            return '立项信息错误'
        # 对应的立项不应有子项
        children_Count = Init_data[0].get('子项数量') or 0
        if children_Count:
            return '对应的立项不应有子项，请重新选择立项信息'
        # 预算控制价不应超过项目概算
        control_price = float(data.get('预算控制价') or 0)
        estimate = float(Init_data[0].get('项目概算') or 0)
        flag = control_price > estimate or control_price < 0
        if flag:
            return '<预算控制价>(%f)输入错误，请将值设置为[0, <项目概算>(%f)]之间' % (control_price, estimate)
        # 中标价不应超过预算控制价
        bid_price = float(data.get('中标价') or 0)
        control_price = float(data.get('预算控制价') or 0)
        flag = bid_price > control_price or bid_price < 0
        if flag:
            return '<中标价>(%f)输入错误，请将值设置为[0, <预算控制价>(%f)]之间' % (bid_price, control_price)
        # update
        if UDID > 0:
            # 确保该项存在
            flag = not table_Bidding.objects.filter(招标识别码=UDID)
            if flag:
                return '招标识别码为<%d>的记录尚不存在，无法修改，请检查' % UDID
            # 正戏
            flag = table_Bidding.objects.filter(
                招标识别码__exact=UDID).update(**data)
            if flag:
                return 'Done'
        # insert
        else:
            # 正戏
            flag = table_Bidding.objects.create(**data)
            if flag:
                return 'Done'
    except Exception as e:
        return str(e)

# 合同管理


def read_For_Contract_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
                 (SELECT           A.合同识别码, A.立项识别码, 项目名称, 分项名称, 项目概算,
                                   I.建设单位识别码, U7.单位名称 AS 建设单位名称, I.代建单位识别码, U8.单位名称 AS 代建单位名称,
                                   A.招标识别码, 招标方式,
                                   B.招标单位识别码, U5.单位名称 AS 招标单位名称, B.中标单位识别码, U6.单位名称 AS 中标单位名称,
                                   合同编号, 合同名称, 合同主要内容, 合同类别,
                                   甲方识别码, U1.单位名称 AS 甲方单位名称, 乙方识别码, U2.单位名称 AS 乙方单位名称,
                                   丙方识别码, U3.单位名称 AS 丙方单位名称, 丁方识别码, U4.单位名称 AS 丁方单位名称,
                                   中标价, 合同值_签订时, 合同值_最新值, 合同值_最终值,
                                   已付款, 已付款/项目概算 AS 已付款占概算,
                                   已付款/合同值_最新值 AS 已付款占合同, 形象进度, 支付上限, 合同签订时间,
                                   开工时间, 竣工合格时间, 保修结束时间, 审计完成时间, 合同备注
                  FROM             tabel_合同信息 AS A
                       LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                       LEFT JOIN   tabel_单位信息 AS U1 ON A.甲方识别码=U1.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U2 ON A.乙方识别码=U2.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U3 ON A.丙方识别码=U3.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U4 ON A.丁方识别码=U4.单位识别码
                       LEFT JOIN   tabel_招标信息 AS B ON A.招标识别码=B.招标识别码
                       LEFT JOIN   tabel_单位信息 AS U5 ON B.招标单位识别码=U5.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U6 ON B.中标单位识别码=U6.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U7 ON I.建设单位识别码=U7.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U8 ON I.代建单位识别码=U8.单位识别码
                       LEFT JOIN   (SELECT 合同识别码, SUM(本次付款额) AS 已付款 FROM tabel_付款信息 GROUP BY 合同识别码) AS P ON A.合同识别码=P.合同识别码
                  ) AS Origin
          '''.format(', '.join(uc.ContractColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)


def new_read_For_Contract_GridDialog(column_name='', comparison=None, operator='='):
    '''
        使用pandas来分析orm得来的数据库原始记录，得到前端需要的数据
        func('立项识别码', 42)
        func('立项识别码', [43, 44], 'in')
    '''
    # 从数据库读取原始信息
    qs_Init = table_Initiation.objects.values()
    qs_Company = table_Company.objects.values()
    qs_Bidding = table_Bidding.objects.values()
    qs_Contract = table_Contract.objects.values()
    qs_Payment = table_Payment.objects.values()
    # 将原始信息转化成dataframe格式
    df_Init = pd.DataFrame(list(qs_Init)).fillna('')
    df_Company = pd.DataFrame(list(qs_Company)).fillna('')
    df_Bidding = pd.DataFrame(list(qs_Bidding)).fillna('')
    df_Contract = pd.DataFrame(list(qs_Contract)).fillna('')
    df_Payment = pd.DataFrame(list(qs_Payment)).fillna('')
    df_sumpay = df_Payment[['本次付款额']].groupby(
        df_Payment['合同识别码']).sum().reset_index()  # 按立项识别码聚合本次付款额
    # 开始连接各表
    df = pd.merge(df_Contract, df_Init[['立项识别码', '项目名称', '分项名称', '项目概算', '建设单位识别码', '代建单位识别码']],
                  on='立项识别码', suffixes=('',  '_Init'), how='left')
    df = pd.merge(df, df_Bidding[['招标识别码', '招标方式', '中标价', '招标单位识别码', '中标单位识别码']],
                  on='招标识别码', suffixes=('',  '_Bidding'), how='left')
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='建设单位识别码', right_on='单位识别码', suffixes=('',  '_建设单位'), how='left')
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='代建单位识别码', right_on='单位识别码', suffixes=('',  '_代建单位'), how='left')
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='招标单位识别码', right_on='单位识别码', suffixes=('',  '_招标单位'), how='left')
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='中标单位识别码', right_on='单位识别码', suffixes=('',  '_中标单位'), how='left')
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='甲方识别码', right_on='单位识别码', suffixes=('',  '_甲方单位'), how='left')
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='乙方识别码', right_on='单位识别码', suffixes=('',  '_乙方单位'), how='left')
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='丙方识别码', right_on='单位识别码', suffixes=('',  '_丙方单位'), how='left')
    df = pd.merge(df, df_Company[['单位识别码', '单位名称']],
                  left_on='丁方识别码', right_on='单位识别码', suffixes=('',  '_丁方单位'), how='left')
    df['建设单位名称'] = df['单位名称']
    df['代建单位名称'] = df['单位名称_代建单位']
    df['招标单位名称'] = df['单位名称_招标单位']
    df['中标单位名称'] = df['单位名称_中标单位']
    df['甲方单位名称'] = df['单位名称_甲方单位']
    df['乙方单位名称'] = df['单位名称_乙方单位']
    df['丙方单位名称'] = df['单位名称_丙方单位']
    df['丁方单位名称'] = df['单位名称_丁方单位']
    df = pd.merge(df, df_sumpay,
                  on='合同识别码', suffixes=('',  '合同已付'), how='left')
    df['已付款'] = df['本次付款额']

    def flag(x1, x2):
        if not x1:
            return 0
        elif x2:
            return float(x1) / float(x2)
        else:
            return None
    df['已付款占概算'] = pd.DataFrame(list(map(flag, df['已付款'], df['项目概算'])))
    df['已付款占合同'] = pd.DataFrame(list(map(flag, df['已付款'], df['合同值_最新值'])))
    result = df[uc.ContractColLabels].fillna('')
    if column_name and operator == '=':
        result = result[result[column_name] == comparison]
    elif column_name and operator == 'in':
        result = result[result[column_name].isin(comparison)]
    result = result.to_dict('records')
    result = sorted(result, key=lambda x: x.get('立项识别码'), reverse=False)
    return result

def old_save_For_Contract_GridDialog(**data):
    '''
        This function can insert/update data for table_Contract.
        input data({'合同识别码': 1, '合同名称': '建设工程XX合同', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    # 参数合法性校验
    if not data:
        return '您未输入任何数据'
    # 参数数量校验
    if len(data) != len(uc.ContractFields):
        return '参数数量(%d)错误，应为(%d)个' % (len(data), len(uc.ContractFields))
    # 确保UDID是整数
    try:
        UDID = int(data.get('招标识别码') or 0)
    except Exception as e:
        return str(e)
    # 确保传入的参数类型正确
    dict_type = dict(zip(uc.ContractFields, uc.ContractFields_Type))
    for field, value in data.items():
        if field not in uc.ContractFields:
            return '无法存储<%s>，请重新输入' % field
        _type = dict_type.get(field)
        if (_type == '整数型' and not (type(value) == type(1) or value is None))\
                or (_type == '浮点型' and not (type(value) == type(1.0) or type(value) == type(1) or type(value) == type(decimal.Decimal(1.0)) or value is None))\
                or (_type == '字符串型' and not (type(value) == type('abc') or value is None))\
                or (_type == '文本型' and not (type(value) == type('abc') or value is None)):
            return '<%s:%s>类型(%s)错误，应为<%s>，请检查' % (field, str(value), str(type(value)), _type)
        elif _type == '日期型':
            try:
                data[field] = datetime.date(
                    *list(time.strptime(data.get(field), "%Y-%m-%d"))[:3])
            except Exception as e:
                return str(e)
    # 判断应该用insert还是update
    try:
        # 立项识别码必须存在、对应的立项必须存在
        InitUDID = data.get('立项识别码') or 0
        Init_data = read_For_Initiation_GridDialog(
            'WHERE 立项识别码=%s', [InitUDID])
        flag = not (InitUDID and Init_data)
        if flag:
            return '立项信息错误'
        # 对应的立项不应有子项
        children_Count = Init_data[0].get('子项数量') or 0
        if children_Count:
            return '对应的立项不应有子项，请重新选择立项信息'
        # 招标识别码如果存在，应有对应招标项，招标项如果存在，应与立项信息相对应
        BiddingUDID = data.get('招标识别码') or 0
        Bidding_data = read_For_Bidding_GridDialog(
            'WHERE 招标识别码=%s', [BiddingUDID])
        flag = not (BiddingUDID and Bidding_data)
        if flag:
            return '招标信息错误'
        # 合同签订值应>=0，招标项如果存在，<=中标价，否则应<=项目概算
        sign_price = float(data.get('合同值_签订时') or 0)
        estimate = float(Init_data.get('项目概算') or 0)
        bid_price = float(Bidding_data.get('中标价') or 0)
        if Bidding_data:
            flag = sign_price < 0 or sign_price > bid_price
            if flag:
                return '<合同值_签订时>(%f)输入错误，请将值设置为[0, <中标价>(%f)]之间' % (sign_price, bid_price)
        else:
            flag = sign_price < 0 or sign_price > estimate
            if flag:
                return '<合同值_签订时>(%f)输入错误，请将值设置为[0, <项目概算>(%f)]之间' % (sign_price, estimate)
        # 合同最终值应不应<0
        final_price = float(data.get('合同值_最终值') or 0)
        flag = final_price < 0
        if flag:
            return '<合同值_最终值>(%f)输入错误，请将值设置为非负数' % final_price
        # 预算控制价不应超过项目概算
        # ======================================写到这儿啦===================================================================
        # 支付上限应<=合同最新值，>=合同已付款(若无该项，则为0)
        # 当合同最终值不存在时，合同最新值应>=项目已付款(若无该项，则为0)，<=项目概算，否则应=项目最终值
        # update
        if UDID > 0:
            # 确保该项存在
            flag = not table_Contract.objects.filter(合同识别码=UDID)
            if flag:
                return '合同识别码为<%d>的记录尚不存在，无法修改，请检查' % UDID
            # 正戏
            flag = table_Contract.objects.filter(
                合同识别码__exact=UDID).update(**data)
            if flag:
                return 'Done'
        # insert
        else:
            # 正戏
            flag = table_Contract.objects.create(**data)
            if flag:
                return 'Done'
    except Exception as e:
        return str(e)
# 分包合同管理


def read_For_SubContract_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
             (SELECT           分包合同识别码, A.立项识别码, 项目名称, 分项名称, A.合同识别码, 合同编号 AS 总包合同编号,
                               合同名称 AS 总包合同名称, 合同主要内容 AS 总包合同主要内容, 合同类别 AS 总包合同类别,
                               合同值_最新值 AS 总包合同值, 分包合同编号, 分包合同名称, 分包合同主要内容, 分包合同类别,
                               A.甲方识别码, U1.单位名称 AS 甲方单位名称, A.乙方识别码, U2.单位名称 AS 乙方单位名称,
                               A.丙方识别码, U3.单位名称 AS 丙方单位名称, A.丁方识别码, U4.单位名称 AS 丁方单位名称,
                               B.甲方识别码 AS 总包甲方识别码, U5.单位名称 AS 总包甲方单位名称, B.乙方识别码 AS 总包乙方识别码, U6.单位名称 AS 总包乙方单位名称,
                               B.丙方识别码 AS 总包丙方识别码, U7.单位名称 AS 总包丙方单位名称, B.丁方识别码 AS 总包丁方识别码, U8.单位名称 AS 总包丁方单位名称,
                               分包合同签订时间, 分包合同值_签订时, 分包合同值_最新值, 分包合同值_最终值, 分包合同备注
              FROM             tabel_分包合同信息 AS A
                   LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                   LEFT JOIN   tabel_合同信息 AS B ON A.合同识别码=B.合同识别码
                   LEFT JOIN   tabel_单位信息 AS U1 ON A.甲方识别码=U1.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U2 ON A.乙方识别码=U2.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U3 ON A.丙方识别码=U3.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U4 ON A.丁方识别码=U4.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U5 ON B.甲方识别码=U5.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U6 ON B.乙方识别码=U6.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U7 ON B.丙方识别码=U7.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U8 ON B.丁方识别码=U8.单位识别码) AS Origin
          '''.format(', '.join(uc.SubContractColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)

# 变更管理


def read_For_Alteration_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
             (SELECT           变更识别码, A.立项识别码, 项目名称, 分项名称, A.合同识别码, 合同编号,
                               合同名称, 合同类别, 合同值_签订时, 甲方识别码, U1.单位名称 AS 甲方单位名称, 乙方识别码, U2.单位名称 AS 乙方单位名称,
                               丙方识别码, U3.单位名称 AS 丙方单位名称, 丁方识别码, U4.单位名称 AS 丁方单位名称,
                               变更类型, 变更编号, 变更主题, 变更登记日期, 变更生效日期,
                               变更原因, 预估变更额度, 预估变更额度/合同值_签订时 AS 预估变更率, 变更额度, 变更额度/合同值_签订时 AS 变更率, 变更备注
              FROM             tabel_变更信息 AS A
                   LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                   LEFT JOIN   tabel_合同信息 AS C ON A.合同识别码=C.合同识别码
                   LEFT JOIN   tabel_单位信息 AS U1 ON C.甲方识别码=U1.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U2 ON C.乙方识别码=U2.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U3 ON C.丙方识别码=U3.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U4 ON C.丁方识别码=U4.单位识别码) AS Origin
          '''.format(', '.join(uc.AlterationColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)

# 预算管理


def read_For_Budget_GridDialog(where_sql='', where_list=[], order_sql='ORDER BY 预算识别码', order_list=[]):
    # 预自建过程
    sql1 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_UDID_table (预算识别码 INT);
        '''
    sql2 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_pay_table (预算识别码 INT, 已分配预算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql2_5 = '''
        CREATE TEMPORARY TABLE IF NOT EXISTS tmp_parent_pay_table (预算识别码 INT, 已分配预算 DECIMAL(12, 2), 已付款 DECIMAL(12, 2));
        '''
    sql3 = '''
        TRUNCATE TABLE tmp_UDID_table;
        '''
    sql4 = '''
        TRUNCATE TABLE tmp_pay_table;
        '''
    sql4_5 = '''
        TRUNCATE TABLE tmp_parent_pay_table;
        '''
    # 将自身的立项识别码及全部子项的立项识别码导入表tmp_UDID_table
    sql5 = '''
        DROP PROCEDURE IF EXISTS get_all_children;
        '''
    sql6 = '''
        CREATE PROCEDURE `get_all_children` (areaId INT)
        BEGIN
            DECLARE sTemp VARCHAR(4000);
            DECLARE sTempChd VARCHAR(4000);
            SET sTemp = '$';
            SET sTempChd = cast(areaId as char);
            INSERT INTO tmp_UDID_table (预算识别码) VALUES(areaId);
            WHILE sTempChd is not NULL DO
                SET sTemp = CONCAT(sTemp,',',sTempChd);
                INSERT INTO tmp_UDID_table (预算识别码) SELECT 预算识别码 FROM tabel_预算信息 WHERE FIND_IN_SET(父项预算识别码,sTempChd)>0;
                SELECT group_concat(预算识别码) INTO sTempChd FROM tabel_预算信息 WHERE FIND_IN_SET(父项预算识别码,sTempChd)>0;
            END WHILE;
        END;
    '''
    # 遍历预算信息表，将预算识别码-项下已付款存入临时表tmp_pay_table
    sql7 = '''
        drop procedure if exists proc_tmp;
        '''
    sql8 = '''
        create procedure `proc_tmp`()
        BEGIN
            declare done int default 0;
            declare UDID bigint;
            declare idCur cursor for select 预算识别码 from tabel_预算信息 ORDER BY 预算识别码;
            declare continue handler for not FOUND set done = 1;
            open idCur;
            REPEAT
                fetch idCur into UDID;
                if not done THEN
                    TRUNCATE TABLE tmp_UDID_table;
                    CALL get_all_children(UDID);
                    INSERT INTO tmp_pay_table (预算识别码, 已分配预算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(预算总额) FROM tabel_预算信息 WHERE 父项预算识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 预算识别码 IN (SELECT 预算识别码 FROM tmp_UDID_table));
                    INSERT INTO tmp_parent_pay_table (预算识别码, 已分配预算, 已付款)
                        (SELECT UDID,
                        (SELECT SUM(预算总额) FROM tabel_预算信息 WHERE 父项预算识别码=UDID),
                        ifnull(SUM(本次付款额),0) FROM tabel_付款信息 WHERE 预算识别码 IN (SELECT 预算识别码 FROM tmp_UDID_table));
                end if;
            until done end repeat;
            close idCur;
        END;
        '''
    sql9 = '''
        CALL proc_tmp();
    '''
    # 正式
    sql = '''SELECT {} FROM
             (SELECT           A.预算识别码, A.预算名称, A.预算周期, A.预算总额,
                               A.父项预算识别码, B.预算名称 AS 父项预算名称, B.预算周期 AS 父项预算周期, 预算子项数量,
                               B.预算总额 AS 父项预算额,
                               ifnull(B.预算总额, 0)-ifnull(TP.已分配预算, 0)+ifnull(A.预算总额, 0) AS 预算上限,
                               T.已分配预算, A.预算总额-T.已分配预算 AS 未分配预算, T.已分配预算/A.预算总额 AS 预算分配比,
                               T.已付款 AS 预算已付额, A.预算总额-T.已付款 AS 预算余额, T.已付款/A.预算总额 AS 预算已付比,
                               A.预算备注
              FROM             tabel_预算信息 AS A
                   LEFT JOIN   tabel_预算信息 AS B  ON A.父项预算识别码=B.预算识别码
                   LEFT JOIN   (SELECT 父项预算识别码, COUNT(*) AS 预算子项数量 FROM tabel_预算信息 GROUP BY 父项预算识别码) AS C ON A.预算识别码=C.父项预算识别码
                   LEFT JOIN   tmp_pay_table AS T ON A.预算识别码=T.预算识别码
                   LEFT JOIN   tmp_parent_pay_table AS TP ON A.父项预算识别码=TP.预算识别码
                   ) AS Origin
          '''.format(', '.join(uc.BudgetColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql1)
    with connection.cursor() as cursor:
        cursor.execute(sql2)
    with connection.cursor() as cursor:
        cursor.execute(sql2_5)
    with connection.cursor() as cursor:
        cursor.execute(sql3)
    with connection.cursor() as cursor:
        cursor.execute(sql4)
    with connection.cursor() as cursor:
        cursor.execute(sql4_5)
    with connection.cursor() as cursor:
        cursor.execute(sql5)
    with connection.cursor() as cursor:
        cursor.execute(sql6)
    with connection.cursor() as cursor:
        cursor.execute(sql7)
    with connection.cursor() as cursor:
        cursor.execute(sql8)
    with connection.cursor() as cursor:
        cursor.execute(sql9)
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)


def read_Budget_For_TreeList():
    # 正式
    sql = '''SELECT 预算识别码 AS Id, CONCAT(ifnull(预算名称, ''), ifnull(预算周期, '')) AS name, 父项预算识别码 AS PId
               FROM tabel_预算信息
           ORDER BY 预算识别码
          '''
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return dictfetchall(cursor)


def format_Budget_Details_By_Tree():
    sql1 = '''SELECT 预算识别码, 预算名称, 预算周期, 预算总额 FROM tabel_预算信息'''
    sql2 = '''SELECT 预算识别码, 父项预算识别码 FROM tabel_预算信息'''
    with connection.cursor() as cursor:
        cursor.execute(sql1)
        data = list(map(list, cursor.fetchall()))
        cursor.execute(sql2)
        hierarchy = list(map(list, cursor.fetchall()))
    # 将列表形式的数据格式化成字典型的
    dict_data = {}
    for da in data:
        dict_data[da[0]] = da[1:]
    # 将层级数据结构转化为dataframe
    array_hierarchy = np.array(hierarchy)
    frame_hierarchy = pd.DataFrame(
        array_hierarchy, columns=['预算识别码', '父项预算识别码'])

    def get_All_Roots():
        frame = frame_hierarchy[frame_hierarchy['父项预算识别码'].isnull()]
        list_frame = frame['预算识别码'].values.tolist()
        return [[x, 0] for x in list_frame]

    def get_All_Children(UDID, deep=0):
        frame = frame_hierarchy[frame_hierarchy['父项预算识别码'] == UDID]
        list_frame = frame['预算识别码'].values.tolist()
        return [[x, deep + 1] for x in list_frame]
    # 开始迭代获取数据层级
    roots_info = get_All_Roots()
    # 访问这些根节点，取得每个根节点的所有子项，存入其中

    def zipLeaves(roots_info):
        for i in range(len(roots_info)):
            UDID = roots_info[i][0]
            deep = roots_info[i].pop()
            roots_info[i] += dict_data[UDID] + [deep]
            children = get_All_Children(UDID, deep)
            roots_info[i] = [roots_info[i]]
            if children:
                roots_info[i].append(children)
                zipLeaves(children)
    zipLeaves(roots_info)
    return roots_info

# 付款管理


def read_For_Payment_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM
             (SELECT           A.付款识别码, 付款登记时间, 付款支付时间, A.立项识别码, I.项目名称, I.分项名称,
                               A.合同识别码, 合同名称, 合同类别, 合同编号, 付款批次, 付款事由,
                               A.付款单位识别码, U1.单位名称 AS 付款单位名称, U1.银行账号 AS 付款单位账号,
                               A.收款单位识别码, U2.单位名称 AS 收款单位名称, U2.银行账号 AS 收款单位账号,
                               I.建设单位识别码, U3.单位名称 AS 建设单位名称, I.代建单位识别码, U4.单位名称 AS 代建单位名称,
                               BI.招标单位识别码, U5.单位名称 AS 招标单位名称, BI.中标单位识别码, U6.单位名称 AS 中标单位名称,
                               C.甲方识别码, U7.单位名称 AS 甲方单位名称, C.乙方识别码, U8.单位名称 AS 乙方单位名称,
                               C.丙方识别码, U9.单位名称 AS 丙方单位名称, C.丁方识别码, U10.单位名称 AS 丁方单位名称,
                               A.预算识别码, 预算名称, 预算周期, 付款时预算总额, 付款时项目概算, 付款时合同付款上限,
                               付款时合同值, 合同值_最终值 AS 合同最终值,
                               付款时预算余额, 付款时概算余额, 付款时合同可付余额, 付款时合同未付额,
                               付款时预算已付额, 付款时合同已付额, 付款时概算已付额,
                               付款时预算已付额/付款时预算总额 AS 付款时预算已付比,
                               付款时合同已付额/付款时合同值 AS 付款时合同已付比,
                               付款时概算已付额/付款时项目概算 AS 付款时概算已付比,
                               付款时形象进度, 本次付款额,
                               本次付款额/付款时预算总额 AS 预算本次付款比,
                               本次付款额/付款时合同值 AS 合同本次付款比,
                               本次付款额/付款时项目概算 AS 概算本次付款比,
                               (本次付款额+付款时预算已付额)/付款时预算总额 AS 预算累付比,
                               (本次付款额+付款时合同已付额)/付款时合同值 AS 合同累付比,
                               (本次付款额+付款时概算已付额)/付款时项目概算 AS 概算累付比,
                               付款备注
              FROM             tabel_付款信息 AS A
                    LEFT JOIN  tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                    LEFT JOIN  tabel_招标信息 AS BI ON A.立项识别码=BI.立项识别码
                    LEFT JOIN  tabel_合同信息 AS C ON A.合同识别码=C.合同识别码
                    LEFT JOIN  (SELECT 立项识别码, 付款识别码, convert(rank , SIGNED) AS 付款批次
                                FROM (SELECT ff.立项识别码, ff.付款识别码, IF(@pa = ff.立项识别码, @rank:=@rank + 1, @rank:=1) AS rank, @pa:=ff.立项识别码
                                      FROM   (SELECT 立项识别码, 付款识别码
                                              FROM   tabel_付款信息
                                              GROUP BY 立项识别码 , 付款识别码
                                              ORDER BY 立项识别码 , 付款识别码) ff, (SELECT @rank:=0, @pa := NULL) tt) result) AS BP ON A.付款识别码=BP.付款识别码
                    LEFT JOIN  tabel_单位信息 AS U1 ON A.付款单位识别码=U1.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U2 ON A.收款单位识别码=U2.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U3 ON I.建设单位识别码=U3.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U4 ON I.代建单位识别码=U4.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U5 ON BI.招标单位识别码=U5.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U6 ON BI.中标单位识别码=U6.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U7 ON C.甲方识别码=U7.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U8 ON C.乙方识别码=U8.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U9 ON C.丙方识别码=U9.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U10 ON C.丁方识别码=U10.单位识别码
                    LEFT JOIN  tabel_预算信息 AS B ON A.预算识别码=B.预算识别码) AS Origin
          '''.format(', '.join(uc.PaymentColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return dictfetchall(cursor)

# 其余查询API


def get_Children_Count(UDID):
    '''
        make sure UDID is int.
        get the count of a clicked item's children.
        return int or None.
    '''
    try:
        UDID = int(UDID)
        return len(table_Initiation.objects.filter(父项立项识别码=UDID))
    except:
        return


def get_Budget_Children_Count(UDID):
    '''
        make sure UDID is int.
        get the count of a clicked item's budget children.
        return int or None.
    '''
    try:
        UDID = int(UDID)
        return len(table_Budget.objects.filter(父项预算识别码=UDID))
    except:
        return


def new_get_All_Grandchildren_UDID(UDID):
    '''
        make sure UDID is int.
        取得某项下全部后代的立项识别码
        return a list(filled by int) or a blank list.
    '''
    db_Id_PId = pd.DataFrame(
        list(table_Initiation.objects.values('立项识别码', '父项立项识别码')))

    def getChildren(UDID):
        return list(db_Id_PId[db_Id_PId.父项立项识别码 == UDID].立项识别码)

    def getGrandChildren(UDID):
        result = []
        children_UDID = getChildren(UDID)
        if children_UDID:       # 如果UDID下还有子项
            for x in children_UDID:
                result += getGrandChildren(x)
            return result + [UDID]
        else:           # 如果UDID为叶子
            return [UDID]

    result = getGrandChildren(UDID)
    result.remove(UDID)
    result.sort()
    return result


def get_All_Grandchildren_UDID(UDID):
    '''
        make sure UDID is int.
        取得某项下全部后代的立项识别码
        return a list(filled by int) or a blank list.
    '''
    try:
        UDID = int(UDID)
        sql = '''
              SELECT queryChildrenAreaInfo(%s);
              CREATE FUNCTION `queryChildrenAreaInfo` (areaId INT)
              RETURNS VARCHAR(4000)
              BEGIN
                  DECLARE sTemp VARCHAR(4000);
                  DECLARE sTempChd VARCHAR(4000);
                  SET sTemp = '$';
                  SET sTempChd = cast(areaId as char);
                  WHILE sTempChd is not NULL DO
                      SET sTemp = CONCAT(sTemp,',',sTempChd);
                      SELECT group_concat(立项识别码) INTO sTempChd FROM tabel_立项信息 where FIND_IN_SET(父项立项识别码,sTempChd)>0;
                  END WHILE;
                  return sTemp;
              END;
              '''
        sql_list = [UDID]
        with connection.cursor() as cursor:
            cursor.execute(sql, sql_list)
            fetchall = cursor.fetchall()[0][0].split(',')[2:]
            return list(map(lambda x: int(x), fetchall))
    except:
        return []


def new_get_All_Budget_Grandchildren_UDID(UDID):
    '''
        取得某预算下全部子项、孙项等的预算识别码
    '''
    db_Id_PId = pd.DataFrame(
        list(table_Budget.objects.values('预算识别码', '父项预算识别码')))

    def getChildren(UDID):
        return list(db_Id_PId[db_Id_PId.父项预算识别码 == UDID].预算识别码)

    def getGrandChildren(UDID):
        result = []
        children_UDID = getChildren(UDID)
        if children_UDID:       # 如果UDID下还有子项
            for x in children_UDID:
                result += getGrandChildren(x)
            return result + [UDID]
        else:           # 如果UDID为叶子
            return [UDID]

    result = getGrandChildren(UDID)
    result.remove(UDID)
    result.sort()
    return result


def get_All_Budget_Grandchildren_UDID(UDID):
    '''
        取得某预算下全部子项、孙项等的预算识别码
    '''
    try:
        UDID = int(UDID)
        sql1 = '''
              set global log_bin_trust_function_creators=1;
              DROP FUNCTION IF EXISTS queryBudgetChildrenAreaInfo;
              '''
        sql2 = '''
              CREATE FUNCTION `queryBudgetChildrenAreaInfo` (areaId INT)
              RETURNS VARCHAR(4000)
              BEGIN
                  DECLARE sTemp VARCHAR(4000);
                  DECLARE sTempChd VARCHAR(4000);
                  SET sTemp = '$';
                  SET sTempChd = cast(areaId as char);
                  WHILE sTempChd is not NULL DO
                      SET sTemp = CONCAT(sTemp,',',sTempChd);
                      SELECT group_concat(预算识别码) INTO sTempChd FROM tabel_预算信息 where FIND_IN_SET(父项预算识别码,sTempChd)>0;
                  END WHILE;
                  return sTemp;
              END;
              '''
        sql = '''SELECT queryBudgetChildrenAreaInfo(%s);'''
        sql_list = [UDID]
        with connection.cursor() as cursor:
            cursor.execute(sql1)
            cursor.execute(sql2)
            cursor.execute(sql, sql_list)
            fetchall = cursor.fetchall()[0][0].split(',')[2:]
            return list(map(lambda x: int(x), fetchall))
    except:
        return []


def get_Count_Payment(list_UDID):
    '''
        make sure UDID is list with int.
        get the count of payment times.
        return int or None.
    '''
    try:
        assert type(list_UDID) == type([])
        return len(table_Payment.objects.filter(立项识别码__in=list_UDID))
    except:
        return


def get_Sum_Money_Payment(list_UDID):
    '''
        make sure UDID is list with int.
        get the sum money of payment.
        return float or None.
    '''
    try:
        assert type(list_UDID) == type([])
        return float(sum([x.get('本次付款额') for x in list(table_Payment.objects.filter(立项识别码__in=list_UDID).values('本次付款额'))]))
    except:
        return


# 权限相关类

class getUserPermission():
    '''
        Check a user wether has a permission.
        Obj(username).func() returns True or False.
    '''

    def __init__(self, username=''):
        '''
            Initialize a object by a user's username
        '''
        self.__filterObj = table_Permission.objects.filter(
            用户名__exact=str(username))

    def user_Is_Exist(self):
        '''
            Judge a user whether exist.
        '''
        if self.__filterObj:
            self.__filterDict = self.__filterObj.values()[0]
            return True
        else:
            return False

    # 以下为打开网页或窗口的权限

    def can_Visit_Overview(self):
        '''
            If a user is exist, and his field(查看数据概览) is True, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        return self.__filterDict.get('查看数据概览')

    def can_Visit_Table(self, classify=''):
        '''
            If a user is exist, and his field(查看XX信息) is True, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        return self.__filterDict.get('查看%s信息' % classify)

    def can_Visit_Attachment(self, classify=''):
        '''
            If a user is exist, and his field(查看单位信息) >= 2, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        return (self.__filterDict.get('查看%s信息' % classify) or 0) >= 2

    # 读取数据权限

    def can_Read_Overview(self):
        '''
            If a user is exist, and his field(查看数据概览) is True, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        return self.__filterDict.get('查看数据概览')

    def can_Read_Table(self, classify=''):
        '''
            If a user is exist, and his field(查看XX信息) is True, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        return self.__filterDict.get('查看%s信息' % classify)

    def can_Get_Attachment_List(self, classify=''):
        '''
            If a user is exist, and his field(查看XX信息) is >= 2, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        return (self.__filterDict.get('查看%s信息' % classify) or 0) >= 2

    def can_Download_Attachment(self, classify=''):
        '''
            If a user is exist, and his field(查看XX信息) is >= 3, then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        return (self.__filterDict.get('查看%s信息' % classify) or 0) >= 3

    # 写入数据权限

    def can_Upload_Attachment(self, classify='', UDID=0):
        '''
            If a user is exist, and his field(操作XX信息) is True,
            or his field(允许操作XX的项目) contains the project,
            then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        classify_dict = {
            # [x, y]
            # x代表classfity对应的表名
            # y==0代表检验权限不需用到project，y==1则反之
            '':         [0,                    0, ],
            '单位':     ['操作单位信息',         1, ],
            '立项':     ['允许操作立项的项目',    2, ],
            '招标':     ['允许操作招标的项目',    2, ],
            '合同':     ['允许操作合同的项目',    2, ],
            '预算':     ['操作预算信息',         1, ],
            '付款':     ['允许操作付款的项目',    2, ],
            '变更':     ['允许操作变更的项目',    2, ],
            '分包合同': ['允许操作分包合同的项目', 2, ],
        }
        return True
        # ============= project=查询数据库 ===========================
        field_name, flag = classify_dict[
            classify]      # 看看要查的表是哪一种，需不需要project
        if flag == 1:
            return bool(self.__filterDict.get(field_name))
        elif flag == 2:
            project_list = (self.__filterDict.get(field_name) or '').split('|')
            return bool(project and project in project_list)

    def can_Write_Table(self, classify='', project=''):
        '''
            If a user is exist, and his field(操作XX信息) is True,
            or his field(允许操作XX的项目) contains the project,
            then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        classify_dict = {
            # [x, y]
            # x代表classfity对应的表名
            # y==0代表检验权限不需用到project，y==1则反之
            '':         [0,                    0, ],
            '单位':     ['操作单位信息',         1, ],
            '立项':     ['允许操作立项的项目',    2, ],
            '招标':     ['允许操作招标的项目',    2, ],
            '合同':     ['允许操作合同的项目',    2, ],
            '预算':     ['操作预算信息',         1, ],
            '付款':     ['允许操作付款的项目',    2, ],
            '变更':     ['允许操作变更的项目',    2, ],
            '分包合同': ['允许操作分包合同的项目', 2, ],
            '概算':     ['允许调整概算的项目',    2, ],
            '合同额':   ['允许调整合同额的项目',   2, ],
        }
        field_name, flag = classify_dict[
            classify]      # 看看要查的表是哪一种，需不需要project
        if flag == 1:
            return bool(self.__filterDict.get(field_name))
        elif flag == 2:
            project_list = (self.__filterDict.get(field_name) or '').split('|')
            return bool(project and project in project_list)

    def get_Permission_Write_Table(self):
        '''
            If a user is exist, and his field(操作XX信息) is True,
            or his field(允许操作XX的项目) contains the project,
            then return True.
            Otherwise return False.
        '''
        if not self.user_Is_Exist():
            return False
        return True    # 保留此行则每个用户都可以
        classify_dict = {
            '单位':     '操作单位信息',
            '立项':     '允许操作立项的项目',
            '招标':     '允许操作招标的项目',
            '合同':     '允许操作合同的项目',
            '预算':     '操作预算信息',
            '付款':     '允许操作付款的项目',
            '变更':     '允许操作变更的项目',
            '分包合同': '允许操作分包合同的项目',
            '概算':     '允许调整概算的项目',
            '合同额':   '允许调整合同额的项目',
        }
        result = {}
        for k, v in classify_dict.items():
            result[k] = self.__filterDict.get(v)
        return result

# 操作OSS文件类


class operateOSS():
    '''
        Operation of Ali-OSS2.
    '''
    __bucket_name = 'xilverp'

    def __init__(self):
        '''
            Initialize a object with connecting server.
        '''
        self.signoss()

    def signoss(self):
        '''
            Connecting server.
        '''
        # auth = oss2.Auth('LTAIiM9nh4F41qKR',
        #                  'FIWNICi6h6mJxaPFz5nU4Zu32yraIn')    # 密码为w开头6位，这是主AccessKey
        # AccessKey（上传）： LTAIrkWvDZ8O0uKl OGb9nLoXLTLPr7aijotKxom5cMsEON
        # dowunload： LTAI2EUy5v6DPE5n qW9xhU4wgxCnfLSJ1d8tI76BChMAwh
        # child1： LTAIKgbaM5kVbrv7 WDu796XDmZYDHCTfA36eEVsba54hTo
        # WEB直传: http://oss-demo.aliyuncs.com/oss-h5-upload-js-direct/index.html?spm=5176.doc31925.2.5.Xm9CsO
        # OSS安全令牌：  https://ram.console.aliyun.com/#/role/fastAuthorize?request=%7B%22serviceCode%22:%22OSS%22%7D
        #       AccessKey: LTAIPaFh3fUlBsfe
        #       AccessKeySecret: 2TXRKPMb1EHLQTA7oEn74Ru3s6PlID
        #       RoleArn: acs:ram::1964398227627600:role/aliyunosstokengeneratorrole
        #       RoleSessionName: external-username
        #       DurationSeconds: 3600
        auth = oss2.Auth('LTAIiM9nh4F41qKR',
                         'FIWNICi6h6mJxaPFz5nU4Zu32yraIn')    # 只读AccessKey
        self.bucket = oss2.Bucket(
            auth, 'http://oss-cn-shanghai.aliyuncs.com', self.__bucket_name)

    def listfile(self, classify, UDID):
        '''
            Get a list of all files with given classify(立项/招标/合同/付款/预算 etc.) and UDID.
            Return a list which is filled by a dictionary.
        '''
        webpath = '%s信息/' % classify + '%d/' % UDID
        result = []
        for b in oss2.ObjectIterator(self.bucket, prefix=webpath):
            filename = b.key.replace(webpath, '')
            if filename:
                f_name = b.key.replace(webpath, '')
                try:
                    f_type = f_name.split('.')[-1]
                except:
                    f_type = ''
                f_time = str(datetime.datetime.fromtimestamp(b.last_modified))
                f_size = b.size or 0
                result.append({'文件名': f_name, '文件类型': f_type,
                               '修改时间': f_time, '文件大小': f_size})
        return result

    def get_file_url(self, classify, UDID, filename):
        '''
            Get a URL of a file with given classify(立项/招标/合同/付款/预算 etc.), UDID and filename.
            Return a string which is a URL address.
        '''
        webpath = '%s信息/' % classify + '%d/' % UDID + filename
        result = self.bucket.sign_url('GET', webpath, 300)
        return result

    def get_upload_keys(self, classify='', UDID=0):
        '''
            使用阿里云OSS2，经同前端页面上传文件，需要accessID、policyBase64、signature三段验证
            本函数用于计算上述三段密码
        '''
        # 基础密钥
        accessKey = 'LTAIiM9nh4F41qKR'
        accessKeySecret = 'FIWNICi6h6mJxaPFz5nU4Zu32yraIn'
        host = 'http://{}.oss-cn-shanghai.aliyuncs.com'.format(
            self.__bucket_name)
        # 验证字段
        now = datetime.datetime.utcnow()
        nowS300 = now + datetime.timedelta(seconds=300)
        timeOut = nowS300.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        policy = {
            "expiration": timeOut,
            "conditions": [
                ["content-length-range", 0, 5 * 1024 * 1024 * 1024],  # 文件大小不得>5G
                {"bucket": "xilverp"},
                ["starts-with", "$key", "%s信息/%d/" % (classify, UDID)],
            ],
        }
        policyText = json.dumps(policy).strip()
        policyBase64 = base64.b64encode(
            policyText.encode(encoding='utf-8')).decode()
        h = hmac.new(accessKeySecret.encode(encoding='utf-8'),
                     policyBase64.encode(encoding='utf-8'), hashlib.sha1)
        signature = base64.b64encode(h.digest()).decode()
        return {
            'policy': policy,
            'accessKey': accessKey,
            'policyBase64': policyBase64,
            'signature': signature,
            'host': host,
        }


def get_oss2_token():
    '''
        return a token for uploader.
    '''
    from aliyunsdkcore import client
    from aliyunsdksts.request.v20150401 import AssumeRoleRequest
    import json
    import oss2
    endpoint = 'oss-cn-shanghai.aliyuncs.com'
    bucket_name = 'xilverp'
    access_key_id = 'LTAIiM9nh4F41qKR'
    access_key_secret = 'FIWNICi6h6mJxaPFz5nU4Zu32yraIn'
    role_arn = 'acs:ram::1964398227627600:role/oss-erp-upload'
    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-shanghai')
    req = AssumeRoleRequest.AssumeRoleRequest()
    # 为了简化讨论，这里没有设置Duration、Policy等，更多细节请参考RAM、STS的相关文档。
    req.set_accept_format('json')  # 设置返回值格式为JSON
    req.set_RoleArn(role_arn)
    req.set_RoleSessionName('session-name')
    body = clt.do_action_with_exception(req)
    toekn = json.loads(body)
    return body

# 写操作


def save_Input_Data(classify, **data):
    '''
        Insert or update the user-input data into DB-table.
        Return (1, 'Done') if success, otherwise return (0, 'error info').
    '''
    classify_model_dict = {
        '单位':     table_Company,
        '立项':     table_Initiation,
        '招标':     table_Bidding,
        '合同':     table_Contract,
        '预算':     table_Budget,
        '付款':     table_Payment,
        '变更':     table_Alteration,
        '分包合同':  table_SubContract,
    }
    try:
        UDID = int(data.get(classify + '识别码'))
    except:
        UDID = 0
    try:
        if UDID > 0:        # update
            table_data = {classify + '识别码__exact': UDID}
            flag = classify_model_dict.get(classify).objects.filter(
                **table_data).update(**data)
            if flag:
                return (1, 'Done')
        elif UDID == 0:     # insert
            flag = classify_model_dict.get(classify).objects.create(**data)
            if flag:
                return (1, 'Done')
    except Exception as e:
        return (0, str(e))


def common_Valid_Data(classify, **data):
    '''
        Check the data if valid.
        return (1, 'OK') if valid, otherwise return (0, 'error info').
    '''
    try:
        classify_model_dict = {
            '单位':     table_Company,
            '立项':     table_Initiation,
            '招标':     table_Bidding,
            '合同':     table_Contract,
            '预算':     table_Budget,
            '付款':     table_Payment,
            '变更':     table_Alteration,
            '分包合同':  table_SubContract,
        }
        classify_field_dict = {
            '单位':     uc.CompanyFields,
            '立项':     uc.InitiationFields,
            '招标':     uc.BiddingFields,
            '合同':     uc.ContractFields,
            '预算':     uc.BudgetFields,
            '付款':     uc.PaymentFields,
            '变更':     uc.SubContractFields,
            '分包合同':  uc.AlterationFields,
        }
        classify_type_dict = {
            '单位':     uc.CompanyFields_Type,
            '立项':     uc.InitiationFields_Type,
            '招标':     uc.BiddingFields_Type,
            '合同':     uc.ContractFields_Type,
            '预算':     uc.BudgetFields_Type,
            '付款':     uc.PaymentFields_Type,
            '变更':     uc.SubContractFields_Type,
            '分包合同':  uc.AlterationFields_Type,
        }
        fds = classify_field_dict.get(classify)      # 对应的字段
        tps = classify_type_dict.get(classify)       # 对应的数据类型
        # 检查data的字段以及类型是否与预期相符
        if len(data) != len(fds):
            return (0, '参数数量(%d)错误，应为(%d)个' % (len(data), len(fds)))
        dict_type = dict(zip(fds, tps))
        for field, value in data.items():
            if field not in fds:
                return (0, '无法存储<%s>，请重新输入' % field)
            _type = dict_type.get(field)
            if (_type == '整数型' and not (type(value) == type(1) or value is None))\
                    or (_type == '浮点型' and not (type(value) == type(1.0) or type(value) == type(1) or type(value) == type(decimal.Decimal(1.0)) or value is None))\
                    or (_type == '字符串型' and not (type(value) == type('abc') or value is None))\
                    or (_type == '文本型' and not (type(value) == type('abc') or value is None)):
                return (0, '<%s:%s>类型(%s)错误，应为<%s>，请检查' % (field, str(value), str(type(value)), _type))
            elif _type == '日期型':
                try:
                    if data.get(field):
                        data[field] = datetime.date(
                            *list(time.strptime(data.get(field), "%Y-%m-%d"))[:3])
                except Exception as e:
                    return (0, str(e))
        # 若UDID > 0，查检该项是否存在
        UDID = data.get(classify + '识别码') or 0
        table_data = {classify + '识别码__exact': UDID}
        tb = classify_model_dict.get(classify)      # 对应的models
        if UDID > 0:
            flag = tb.objects.filter(**table_data)
            if not flag:
                return (0, '<%s识别码：%d>对应的记录不存在，请检查' % (classify, UDID))
        # 有无unique列重复
        classify_unique_dict = {
            '单位':     ['单位名称', ],
            '立项':     ['项目名称', '分项名称', ],
            '招标':     [],
            '合同':     [],
            '预算':     ['预算名称', '预算周期'],
            '付款':     [],
            '变更':     [],
            '分包合同':  [],
        }
        uniq_filed = classify_unique_dict.get(classify)
        if uniq_filed:
            table_data = {}
            for field in uniq_filed:
                table_data[field + '__exact'] = data.get(field)
            flag = tb.objects.filter(**table_data)
            if flag:
                unique_UDID = flag.values()[0].get(classify + '识别码')
                if UDID == 0 or UDID != unique_UDID:
                    return (0, '<%s>已存在，请检查' % '-'.join(list(table_data.values())))
        return (1, 'OK')
    except Exception as e:
        return (0, str(e))


def save_For_Company(checkEstimate=True, **data):
    '''
        This function can insert/update data for table_Company.
        input data({'单位识别码': 1, '单位名称': '青岛X公司', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    flag = common_Valid_Data('单位', **data)
    if not flag[0]:
        return flag
    return save_Input_Data('单位', **data)


def save_For_Initiation(checkEstimate=True, **data):
    '''
        This function can insert/update data for table_Initiation.
        input data({'立项识别码': 1, '项目名称': '北王安置房', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    flag = common_Valid_Data('立项', **data)
    if not flag[0]:
        return flag
    try:
        # 如果有父项，项目名称应与父项项目名称一致
        UDID = data.get('立项识别码') or 0
        parentUDID = data.get('父项立项识别码') or 0
        ptb = table_Initiation.objects.filter(
            立项识别码__exact=parentUDID).values()   # 数据库里真有这一项
        flag = parentUDID and ptb
        if flag:
            parent_project = ptb[0].get('项目名称')
            project = data.get('项目名称')
            if project != parent_project:
                return (0, '<项目名称>(%s)与<父项项目名称>(%s)不一致，请修改' % (project, parent_project))
        # 父项应为空，或父项的父项...应为空，否则说明有循环引用象
        UDID = data.get('立项识别码') or 0
        parentUDID = data.get('父项立项识别码') or 0
        for i in range(100):
            if not parentUDID:
                break
            if UDID == parentUDID > 0:
                return (0, '该项存在循环引用现象，请优化项目结构')
            orm_init = table_Initiation.objects.filter(
                立项识别码=parentUDID).values()
            if orm_init:
                parentUDID = orm_init[0].get('父项立项识别码')
            else:
                break
        else:
            return (0, '该项深度过深，请优化项目结构')
        if checkEstimate:
            # 项目概算应>=已付款，项目概算应>=已分配概算
            UDIDs = [UDID] + get_All_Grandchildren_UDID(UDID)
            orm_payment = table_Payment.objects.filter(立项识别码__in=UDIDs)
            payed = float(sum([x.get('本次付款额') for x in orm_payment.values()]))
            estimate = float(data.get('项目概算') or 0)
            if estimate < payed:
                return (0, '<项目概算>(%f)过低，请调整为不低于<概算已付款额>(%f)' % (estimate, payed))
            orm_init = table_Initiation.objects.filter(
                父项立项识别码=UDID).values()
            distributed_estimate = float(
                sum([x.get('项目概算') for x in orm_init]))
            if estimate < distributed_estimate:
                return (0, '<项目概算>(%f)过低，请调整为不低于<已分配概算>(%f)' % (estimate, distributed_estimate))
            # 父项存在时，项目概算应<= 项目概算上限
            parentUDID = data.get('父项立项识别码') or 0
            if parentUDID > 0:
                orm_init = table_Initiation.objects.filter(
                    父项立项识别码=parentUDID).exclude(立项识别码=UDID).values()
                brother_estimate = float(
                    sum([x.get('项目概算') for x in orm_init]))
                parent_estimate = float(table_Initiation.objects.filter(
                    立项识别码=parentUDID).values()[0].get('项目概算'))
                limit_estimate = parent_estimate - brother_estimate
                estimate = float(data.get('项目概算') or 0)
                if estimate > limit_estimate:
                    return (0, '<项目概算>(%f)过高，请调整为不高于(%f)' % (estimate, limit_estimate))
    except Exception as e:
        return (0, str(e))
    # 数据合法后存入数据库
    return save_Input_Data('立项', **data)


def save_For_Bidding(checkEstimate=True, **data):
    '''
        This function can insert/update data for table_Bidding.
        input data({'招标识别码': 1, '招标方式': '公开招标', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    flag = common_Valid_Data('招标', **data)
    if not flag[0]:
        return flag
    try:
        # 立项识别码必须存在、对应的立项必须存在，且不应有子项
        InitUDID = data.get('立项识别码') or 0
        orm_init = table_Initiation.objects.filter(立项识别码=InitUDID).values()
        flag = InitUDID and orm_init
        if not flag:
            return (0, '立项信息错误')
        children = table_Initiation.objects.filter(父项立项识别码=InitUDID).values()
        if children:
            return (0, '对应的立项不应有子项，请重新选择立项信息')
        # 预算控制价不应超过项目概算
        if checkEstimate:
            control_price = float(data.get('预算控制价') or 0)
            estimate = float(orm_init[0].get('项目概算') or 0)
            # 此段检测控制价是否超概算
            # flag = control_price > estimate or control_price < 0
            # if flag:
            #     return (0, '<预算控制价>(%f)输入错误，请将值设置为[0, <项目概算>(%f)]之间' % (control_price, estimate))
            # 此段只检查控制价是否为0
            flag = control_price < 0
            if flag:
                return (0, '<预算控制价>(%f)输入错误，请将值设置为>=0' % (control_price, estimate))
        # 中标价不应超过预算控制价
        bid_price = float(data.get('中标价') or 0)
        control_price = float(data.get('预算控制价') or 0)
        flag = bid_price > control_price or bid_price < 0
        if flag:
            return (0, '<中标价>(%f)输入错误，请将值设置为[0, <预算控制价>(%f)]之间' % (bid_price, control_price))
    except Exception as e:
        return (0, str(e))
    # 数据合法后存入数据库
    return save_Input_Data('招标', **data)


def save_For_Contract(checkEstimate=True, **data):
    '''
        This function can insert/update data for table_Contract.
        input data({'合同识别码': 1, '合同名称': '建设工程XX合同', ...}) which is a dictionary.
        return 'Done' if success;
        return Error Message if failed.
    '''
    flag = common_Valid_Data('合同', **data)
    if not flag[0]:
        return flag
    try:
        # 立项识别码必须存在、对应的立项必须存在，且不应有子项
        InitUDID = data.get('立项识别码') or 0
        orm_init = table_Initiation.objects.filter(立项识别码=InitUDID).values()
        flag = InitUDID and orm_init
        if not flag:
            return (0, '立项信息错误')
        children = table_Initiation.objects.filter(父项立项识别码=InitUDID).values()
        if children:
            return (0, '对应的立项不应有子项，请重新选择立项信息')
        # 招标识别码如果存在，应有对应招标项，招标项如果存在，应与立项信息相对应
        BiddingUDID = data.get('招标识别码') or 0
        orm_bidding = table_Bidding.objects.filter(招标识别码=BiddingUDID).values()
        InitUDID = data.get('立项识别码') or 0
        flag = not BiddingUDID or orm_bidding and orm_bidding[
            0].get('立项识别码') == InitUDID
        if not flag:
            return (0, '招标信息错误')
        # 合同签订值应>=0，<=项目概算，招标项如果存在，<=中标价
        sign_price = float(data.get('合同值_签订时') or 0)
        InitUDID = data.get('立项识别码') or 0
        BiddingUDID = data.get('招标识别码') or 0
        if BiddingUDID:
            orm_bidding = table_Bidding.objects.filter(
                招标识别码=BiddingUDID).values()
            bid_price = float(orm_bidding[0].get('中标价') or 0)
            if not 0 <= sign_price <= bid_price:
                return (0, '<合同值_签订时>(%f)输入错误，请将值设置为[0, <中标价>(%f)]之间' % (sign_price, bid_price))
        if checkEstimate:
            orm_init = table_Initiation.objects.filter(立项识别码=InitUDID).values()
            estimate = float(orm_init[0].get('项目概算') or 0)
            flag = 0 <= sign_price <= estimate
            if not flag:
                return (0, '<合同值_签订时>(%f)输入错误，请将值设置为[0, <项目概算>(%f)]之间' % (sign_price, estimate))
        # 合同最终值应不<0
        final_price = float(data.get('合同值_最终值') or 0)
        if final_price < 0:
            return (0, '<合同值_最终值>(%f)输入错误，请将值设置为>=0' % (final_price,))
        # 支付上限应<=合同最新值，>=合同已付款(若无该项，则为0)
        limit_price = float(data.get('支付上限') or 0)
        last_price = float(data.get('合同值_最新值') or 0)
        ContractUDID = data.get('合同识别码') or 0
        orm_payment = table_Payment.objects.filter(合同识别码=ContractUDID)
        payed = float(sum([x.get('本次付款额') for x in orm_payment.values()]))
        flag = payed <= limit_price <= last_price
        if not flag:
            return (0, '<支付上限>(%f)输入错误，请将值设置为[<合同已付款>(%f), <合同值_最新值>(%f)]之间' % (limit_price, payed, last_price))
        # 当合同最终值不存在时，合同最新值应>=项目已付款(若无该项，则为0)，<=项目概算，否则应=合同最终值
        last_price = float(data.get('合同值_最新值') or 0)
        final_price = float(data.get('合同值_最终值') or 0)
        InitUDID = data.get('立项识别码') or 0
        orm_init = table_Initiation.objects.filter(立项识别码=InitUDID).values()
        estimate = float(orm_init[0].get('项目概算') or 0)
        ContractUDID = data.get('合同识别码') or 0
        orm_payment = table_Payment.objects.filter(合同识别码=ContractUDID)
        payed = float(sum([x.get('本次付款额') for x in orm_payment.values()]))
        if checkEstimate:
            flag = last_price == final_price if final_price else payed <= last_price <= estimate
        else:
            flag = last_price == final_price if final_price else payed <= last_price
        if not flag:
            return (0, '<合同值_最新值>输入错误，请检查')
    except Exception as e:
        return str(e)
    # 数据合法后存入数据库
    return save_Input_Data('合同', **data)


def save_For_SubContract(checkEstimate=True, **data):
    '''
        This function can insert/update data for table_SubContract.
        input data({'分包合同识别码': 1, '分包合同名称': '建设工程XX合同', ...}) which is a dictionary.
        return (1, 'Done') if success;
        return (0, Error Message) if failed.
    '''
    flag = common_Valid_Data('分包合同', **data)
    if not flag[0]:
        return flag
    try:
        # 保证立项存在、合同存在，且立项合同一致
        InitUDID = data.get('立项识别码') or 0
        orm_init = table_Initiation.objects.filter(立项识别码=InitUDID).values()
        flag = InitUDID and orm_init
        if not flag:
            return (0, '立项信息错误')
        ContractUDID = data.get('合同识别码') or 0
        orm_contract = table_Contract.objects.filter(
            合同识别码=ContractUDID).values()
        InitUDID = data.get('立项识别码') or 0
        flag = not ContractUDID or orm_contract and orm_contract[
            0].get('立项识别码') == InitUDID
        if not flag:
            return (0, '合同信息错误')
        # 合同签订值应>=0，<=总包合同签订值
        sign_price_Sub = float(data.get('分包合同值_签订时') or 0)
        ContractUDID = data.get('合同识别码') or 0
        orm_payment = table_Payment.objects.filter(合同识别码=ContractUDID).values()
        sign_price = float(orm_payment[0].get('合同值_签订时') or 0)
        flag = 0 <= sign_price_Sub <= sign_price
        if not flag:
            return (0, '<分包合同值_签订时>(%f)输入错误，请将值设置为[0, <总包合同值_签订时>(%f)]之间' % (sign_price_Sub, sign_price))
        # 合同最终值应不<0
        final_price_Sub = float(data.get('分包合同值_最终值') or 0)
        if final_price_Sub < 0:
            return (0, '<分包合同值_最终值>(%f)输入错误，请将值设置为>=0' % (final_price_Sub,))
        # 当合同最终值存在时，合同值新值=合同最终值
        final_price_Sub = float(data.get('分包合同值_最终值') or 0)
        last_price_Sub = float(data.get('分包合同值_最新值') or 0)
        flag = not final_price_Sub or last_price_Sub == final_price_Sub
        if not flag:
            return (0, '<分包合同值_最新值>输入错误，请检查')
    except Exception as e:
        return (0, str(e))
    return save_Input_Data('分包合同', **data)


def save_For_Alteration(checkEstimate=True, **data):
    '''
        This function can insert/update data for table_Alteration.
        input data({'变更识别码': 1, '变更类型': '批价', ...}) which is a dictionary.
        return (1, 'Done') if success;
        return (0, Error Message) if failed.
    '''
    flag = common_Valid_Data('变更', **data)
    if not flag[0]:
        return flag
    try:
        # 保证立项存在、合同存在，且立项合同一致
        InitUDID = data.get('立项识别码') or 0
        orm_init = table_Initiation.objects.filter(立项识别码=InitUDID).values()
        flag = InitUDID and orm_init
        if not flag:
            return (0, '立项信息错误')
        ContractUDID = data.get('合同识别码') or 0
        orm_contract = table_Contract.objects.filter(
            合同识别码=ContractUDID).values()
        InitUDID = data.get('立项识别码') or 0
        flag = not ContractUDID or orm_contract and orm_contract[
            0].get('立项识别码') == InitUDID
        if not flag:
            return (0, '合同信息错误')
    except Exception as e:
        return (0, str(e))
    return save_Input_Data('变更', **data)


def save_For_Budget(checkEstimate=True, **data):
    '''
        This function can insert/update data for table_Budget.
        input data({'预算识别码': 1, '预算名称': '北王安置房工程款', ...}) which is a dictionary.
        return (1, 'Done') if success;
        return (0, Error Message) if failed.
    '''
    flag = common_Valid_Data('预算', **data)
    if not flag[0]:
        return flag
    try:
        # 父项应为空，或父项的父项...应为空，否则说明有循环引用象
        UDID = data.get('预算识别码') or 0
        parentUDID = data.get('父项预算识别码') or 0
        for i in range(100):
            if not parentUDID:
                break
            if UDID == parentUDID > 0:
                return (0, '该项存在循环引用现象，请优化项目结构')
            orm_budget = table_Budget.objects.filter(
                预算识别码=parentUDID).values()
            if orm_budget:
                parentUDID = orm_budget[0].get('父项预算识别码')
            else:
                break
        else:
            return (0, '该项深度过深，请优化项目结构')
        # 预算总额应>=已付款，还应>=已分配预算
        UDID = data.get('预算识别码') or 0
        UDIDs = [UDID] + get_All_Budget_Grandchildren_UDID(UDID)
        orm_payment = table_Payment.objects.filter(预算识别码__in=UDIDs)
        payed = float(sum([x.get('本次付款额') for x in orm_payment.values()]))
        budget = float(data.get('预算总额') or 0)
        if budget < payed:
            return (0, '<预算总额>(%f)过低，请调整为不低于<预算已付款额>(%f)' % (budget, payed))
        orm_budget = table_Budget.objects.filter(
            父项预算识别码=UDID).values()
        distributed_budget = float(
            sum([x.get('预算总额') for x in orm_budget]))
        if budget < distributed_budget:
            return (0, '<预算总额>(%f)过低，请调整为不低于<已分配预算>(%f)' % (budget, distributed_budget))
        # 父项存在时，预算总额应<= 项目预算上限
        UDID = data.get('预算识别码') or 0
        parentUDID = data.get('父项预算识别码') or 0
        if parentUDID > 0:
            orm_budget = table_Budget.objects.filter(
                父项预算识别码=parentUDID).exclude(预算识别码=UDID).values()
            brother_budget = float(
                sum([x.get('预算总额') for x in orm_budget]))
            parent_budget = float(table_Budget.objects.filter(
                预算识别码=parentUDID).values()[0].get('预算总额'))
            limit_budget = parent_budget - brother_budget
            budget = float(data.get('预算总额') or 0)
            if budget > limit_budget:
                return (0, '<预算总额>(%f)过高，请调整为不高于(%f)' % (budget, limit_budget))
    except Exception as e:
        return (0, str(e))
    return save_Input_Data('预算', **data)


def save_For_Payment(checkEstimate=True, **data):
    '''
        This function can insert/update data for table_Payment.
        input data({'付款识别码': 1, '付款事由': '工程款', ...}) which is a dictionary.
        return (1, 'Done') if success;
        return (0, Error Message) if failed.
    '''
    flag = common_Valid_Data('付款', **data)
    if not flag[0]:
        return flag
    try:
        # 立项识别码必须存在、对应的立项必须存在，且不应有子项
        InitUDID = data.get('立项识别码') or 0
        orm_init = table_Initiation.objects.filter(立项识别码=InitUDID).values()
        flag = InitUDID and orm_init
        if not flag:
            return (0, '立项信息错误')
        children = table_Initiation.objects.filter(父项立项识别码=InitUDID).values()
        if children:
            return (0, '对应的立项不应有子项，请重新选择立项信息')
        # 合同识别码如果存在，应有对应合同项，合同项如果存在，应与立项信息相对应
        ContractUDID = data.get('合同识别码') or 0
        orm_contract = table_Contract.objects.filter(
            合同识别码=ContractUDID).values()
        InitUDID = data.get('立项识别码') or 0
        flag = not ContractUDID or orm_contract and orm_contract[
            0].get('立项识别码') == InitUDID
        if not flag:
            return (0, '合同信息错误')
        if checkEstimate:
            # 本次付款额不得大于概算余额
            InitUDID = data.get('立项识别码') or 0
            orm_init = table_Initiation.objects.filter(立项识别码=InitUDID).values()
            estimate = float(orm_init[0].get('项目概算') or 0)
            PeymentUDID = data.get('付款识别码') or 0
            orm_payment = table_Payment.objects.filter(
                立项识别码=InitUDID).exclude(付款识别码=PeymentUDID).values()
            payed_estimate = float(sum([x.get('本次付款额') for x in orm_payment]))
            remaining_estimate = estimate - payed_estimate
            this_pay = float(data.get('本次付款额') or 0)
            flag = this_pay <= remaining_estimate
            if not flag:
                return (0, '<本次付款额>(%f)输入错误，其值应在[0, <概算余额>(%f)]之间，请调整' % (this_pay, remaining_estimate))
        # 预算不得为空，且本次付款额不得大于预算余额
        BudgetUDID = data.get('预算识别码') or 0
        orm_budget = table_Budget.objects.filter(预算识别码=BudgetUDID).values()
        flag = BudgetUDID and orm_budget
        if not flag:
            return (0, '预算信息错误')
        children = table_Budget.objects.filter(父项预算识别码=BudgetUDID).values()
        if children:
            return (0, '对应的预算不应有子项，请重新选择预算信息')
        budget = float(orm_budget[0].get('预算总额') or 0)
        PeymentUDID = data.get('付款识别码') or 0
        orm_payment = table_Payment.objects.filter(
            预算识别码=BudgetUDID).exclude(付款识别码=PeymentUDID).values()
        payed_budget = float(sum([x.get('本次付款额') for x in orm_payment]))
        remaining_budget = budget - payed_budget
        this_pay = float(data.get('本次付款额') or 0)
        flag = this_pay <= remaining_budget
        if not flag:
            return (0, '<本次付款额>(%f)输入错误，其值应在[0, <预算余额>(%f)]之间，请调整' % (this_pay, remaining_budget))
        # 若合同存在，本次付款额不得大于合同余额
        ContractUDID = data.get('合同识别码') or 0
        if ContractUDID:
            orm_contract = table_Contract.objects.filter(
                合同识别码=ContractUDID).values()
            limit_price = float(orm_contract[0].get('支付上限') or 0)
            PeymentUDID = data.get('付款识别码') or 0
            orm_payment = table_Payment.objects.filter(
                合同识别码=ContractUDID).exclude(付款识别码=PeymentUDID).values()
            payed_contract = float(sum([x.get('本次付款额') for x in orm_payment]))
            remaining_contract = contract - payed_contract
            this_pay = float(data.get('本次付款额') or 0)
            flag = this_pay <= remaining_contract
            if not flag:
                return (0, '<本次付款额>(%f)输入错误，其值应在[0, <合同付款余额>(%f)]之间，请调整' % (this_pay, remaining_contract))
    except Exception as e:
        return str(e)
    # 数据合法后存入数据库
    return save_Input_Data('付款', **data)


# 删除操作

def del_For_All(classify, UDID):
    '''
        This function can delte all records for all tables.
        return (1, 'Done') if success.if
        return (0, Error Message) if failed.
    '''
    classify_model_dict = {
        '单位':     table_Company,
        '立项':     table_Initiation,
        '招标':     table_Bidding,
        '合同':     table_Contract,
        '预算':     table_Budget,
        '付款':     table_Payment,
        '变更':     table_Alteration,
        '分包合同':  table_SubContract,
    }
    try:
        UDID = int(UDID)
    except:
        UDID = 0
    if UDID:
        try:
            table_data = {classify + '识别码': UDID}
            for _, table in classify_model_dict.items():
                try:
                    table.objects.filter(**table_data).delete()
                except:
                    pass
            return (1, 'Done')
        except Exception as e:
            return (0, str(e))
    else:
        return (0, '识别码输入错误')
