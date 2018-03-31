#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-11-06 10:13:37
# @Last Modified by:   Administrator
# @Last Modified time: 2017-12-15 15:39:15

from django.db import connection
import online.userConst as uc
from online.models import *
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
import pandas as pd
import numpy as np
import hashlib
import json
import decimal, datetime

# 格式化字符串
def thousands(n): return '{:>,.2f}'.format(n)
def percents(n): return '{:>.2f}'.format((n or 0) * 100) + '%'

# HASH加密函数
def hash_sha256(string):
    m = hashlib.sha256()
    m.update(string.encode('utf8'))
    return m.hexdigest()
    
# 将对象转化为字典
def classToDict(obj):
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
            try:
                if len(str(obj).split('.')[1]) <= 2:    # 说明是浮点型
                    return thousands(float(obj))
                else:   # 说明是百分比
                    return percents(float(obj))
            except:
                return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# 权限管理
def getPermission(username):
    try:
        return table_Permission.objects.filter(用户名__exact=username).values()[0]
    except:
        return

# 树型数据
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
    sql10 = '''SELECT           I.立项识别码 AS 立项识别码, 项目名称, 分项名称, 合同名称, 项目概算, 
                                  已分配概算/项目概算 AS 概算已分配率, T.已付款/项目概算 AS 概算付款比, 
                                  招标方式, 中标价, 合同值_最新值, P.已付款/合同值_最新值 AS 合同付款比, T.已付款, 分包合同数量
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
        data = list(map(list, cursor.fetchall()))
        cursor.execute(sql11)
        hierarchy = list(map(list, cursor.fetchall()))
    # 将列表形式的数据格式化成字典型的
    dict_data = {}
    for da in data:
        dict_data[da[0]] = da[1:]
    # 将层级数据结构转化为dataframe
    array_hierarchy = np.array(hierarchy)
    frame_hierarchy = pd.DataFrame(array_hierarchy, columns=['立项识别码', '父项立项识别码'])
    def get_All_Roots():
        frame = frame_hierarchy[frame_hierarchy['父项立项识别码'].isnull()]
        list_frame = frame['立项识别码'].values.tolist()
        return [[x, 0] for x in list_frame]
    def get_All_Children(UDID, deep=0):
        frame = frame_hierarchy[frame_hierarchy['父项立项识别码'] == UDID]
        list_frame = frame['立项识别码'].values.tolist()
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

# 单位管理
def read_For_Company_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = 'SELECT {} FROM tabel_单位信息 '.format(', '.join(uc.CompanyColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return [list(x) for x in cursor.fetchall()]

# 立项管理
def read_For_Initiation_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
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
    sql = '''SELECT {} FROM 
             (SELECT           A.立项识别码, A.项目名称, A.分项名称, A.父项立项识别码, B.项目名称 AS 父项项目名称, B.分项名称 AS 父项分项名称,
                               A.建设单位识别码, U1.单位名称 AS 建设单位名称, A.代建单位识别码, U2.单位名称 AS 代建单位名称, 
                               A.立项文件名称, A.立项时间, A.项目概算, A.项目概算-T.已分配概算 AS 未分配概算, T.已付款/A.项目概算 AS 概算付款比, A.立项备注
              FROM             tabel_立项信息 AS A
                   LEFT JOIN   tabel_立项信息 AS B  ON A.父项立项识别码=B.立项识别码
                   LEFT JOIN   tabel_单位信息 AS U1 ON A.建设单位识别码=U1.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U2 ON A.代建单位识别码=U2.单位识别码
                   LEFT JOIN   tmp_pay_table AS T ON A.立项识别码=T.立项识别码) AS Origin
          '''.format(', '.join(uc.InitiationColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql1)
    with connection.cursor() as cursor:
        cursor.execute(sql2)
    with connection.cursor() as cursor:
        cursor.execute(sql3)
    with connection.cursor() as cursor:
        cursor.execute(sql4)
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
        return [list(x) for x in cursor.fetchall()]
def get_All_Grandchildren(UDID):
        '取得某项下全部子项、孙项等的立项识别码'
        sql1 = '''
        	  set global log_bin_trust_function_creators=1;
              DROP FUNCTION IF EXISTS queryChildrenAreaInfo;
              '''
        sql2 =''' 
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
            return list(map(lambda x:int(x), fetchall))

# 招标管理
def read_For_Bidding_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM 
                 (SELECT           招标识别码, A.立项识别码 AS 立项识别码, 项目名称, 分项名称, 招标方式, 招标单位识别码, 
                                   U1.单位名称 AS 招标单位名称, 招标代理识别码, U2.单位名称 AS 招标代理单位名称, 项目概算,
                                   预算控制价, 招标文件定稿时间, 公告邀请函发出时间, 开标时间, 中标通知书发出时间, 
                                   中标单位识别码, U3.单位名称 AS 中标单位名称, 中标价, 招标备注
                  FROM             tabel_招标信息 AS A
                       LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                       LEFT JOIN   tabel_单位信息 AS U1 ON A.招标单位识别码=U1.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U2 ON A.招标代理识别码=U2.单位识别码
                       LEFT JOIN   tabel_单位信息 AS U3 ON A.中标单位识别码=U3.单位识别码) AS Origin
          '''.format(', '.join(uc.BiddingColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        # return dictfetchall(cursor)        
        return [list(x) for x in cursor.fetchall()]

# 合同管理
def read_For_Contract_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM 
                 (SELECT           A.合同识别码, A.立项识别码, 项目名称, 分项名称, 项目概算, A.招标识别码, 招标方式, 合同编号, 合同名称,
                                   合同主要内容, 合同类别, 甲方识别码, U1.单位名称 AS 甲方单位名称, 乙方识别码, U2.单位名称 AS 乙方单位名称, 
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
                       LEFT JOIN   (SELECT 合同识别码, SUM(本次付款额) AS 已付款 FROM tabel_付款信息 GROUP BY 合同识别码) AS P ON A.合同识别码=P.合同识别码) AS Origin
          '''.format(', '.join(uc.ContractColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return [list(x) for x in cursor.fetchall()]

# 分包合同管理
def read_For_SubContract_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM 
             (SELECT           分包合同识别码, A.立项识别码, 项目名称, 分项名称, A.合同识别码, 合同编号 AS 总包合同编号,
                               合同名称 AS 总包合同名称, 合同主要内容 AS 总包合同主要内容, 合同类别 AS 总包合同类别, 
                               合同值_最新值 AS 总包合同值, 分包合同编号, 分包合同名称, 分包合同主要内容, 分包合同类别,
                               A.甲方识别码, U1.单位名称 AS 甲方单位名称, A.乙方识别码, U2.单位名称 AS 乙方单位名称, 
                               A.丙方识别码, U3.单位名称 AS 丙方单位名称, A.丁方识别码, U4.单位名称 AS 丁方单位名称,
                               分包合同签订时间, 分包合同值_签订时, 分包合同值_最新值, 分包合同值_最终值, 分包合同备注
              FROM             tabel_分包合同信息 AS A
                   LEFT JOIN   tabel_立项信息 AS I ON A.立项识别码=I.立项识别码
                   LEFT JOIN   tabel_单位信息 AS U1 ON A.甲方识别码=U1.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U2 ON A.乙方识别码=U2.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U3 ON A.丙方识别码=U3.单位识别码
                   LEFT JOIN   tabel_单位信息 AS U4 ON A.丁方识别码=U4.单位识别码
                   LEFT JOIN   tabel_合同信息 AS B ON A.合同识别码=B.合同识别码) AS Origin
          '''.format(', '.join(uc.SubContractColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return [list(x) for x in cursor.fetchall()]

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
        return [list(x) for x in cursor.fetchall()]

# 预算管理
def read_For_Budget_GridDialog(where_sql='', where_list=[], order_sql='', order_list=[]):
    sql = '''SELECT {} FROM 
             (SELECT           A.预算识别码, A.父项预算识别码, B.预算名称 AS 父项预算名称, A.预算名称, A.预算周期, A.预算总额,
                               已付款 AS 预算已付额, A.预算总额-已付款 AS 预算余额, 已付款/A.预算总额 AS 预算已付比,
                               A.预算备注
              FROM             tabel_预算信息 AS A
                   LEFT JOIN   tabel_预算信息 AS B ON A.父项预算识别码=B.预算识别码
                   LEFT JOIN   (SELECT 预算识别码, SUM(本次付款额) AS 已付款 FROM tabel_付款信息 GROUP BY 预算识别码) AS P ON A.预算识别码=P.预算识别码) AS Origin
          '''.format(', '.join(uc.BudgetColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return [list(x) for x in cursor.fetchall()]
        
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
    frame_hierarchy = pd.DataFrame(array_hierarchy, columns=['预算识别码', '父项预算识别码'])
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
                               A.预算识别码, 预算名称, 预算周期, 付款时预算总额, 付款时项目概算, 付款时合同付款上限,
                               付款时合同值, 付款时预算余额, 付款时概算余额, 付款时合同可付余额, 付款时合同未付额,
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
                    LEFT JOIN  tabel_合同信息 AS C ON A.合同识别码=C.合同识别码
                    LEFT JOIN  (SELECT 立项识别码, 付款识别码, convert(rank , SIGNED) AS 付款批次
                                FROM (SELECT ff.立项识别码, ff.付款识别码, IF(@pa = ff.立项识别码, @rank:=@rank + 1, @rank:=1) AS rank, @pa:=ff.立项识别码
                                      FROM   (SELECT 立项识别码, 付款识别码
                                              FROM   tabel_付款信息
                                              GROUP BY 立项识别码 , 付款识别码
                                              ORDER BY 立项识别码 , 付款识别码) ff, (SELECT @rank:=0, @pa := NULL) tt) result) AS BP ON A.付款识别码=BP.付款识别码
                    LEFT JOIN  tabel_单位信息 AS U1 ON A.付款单位识别码=U1.单位识别码
                    LEFT JOIN  tabel_单位信息 AS U2 ON A.收款单位识别码=U2.单位识别码
                    LEFT JOIN  tabel_预算信息 AS B ON A.预算识别码=B.预算识别码) AS Origin
          '''.format(', '.join(uc.PaymentColLabels)) + where_sql + ' ' + order_sql
    sql_list = where_list + order_list
    with connection.cursor() as cursor:
        cursor.execute(sql, sql_list)
        return [list(x) for x in cursor.fetchall()]