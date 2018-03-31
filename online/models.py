#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class table_User(models.Model):
    '用户表'
    DB_id = models.BigAutoField(primary_key=True, null=False)
    用户名 = models.CharField(max_length=255, null=False, unique=True)
    密码 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.用户名

    class Meta:
        db_table = 'tabel_user'  # 自定义表名称为mytable
        verbose_name = '用户表'  # 指定在admin管理界面中显示的名称
        app_label = 'online'
        ordering = ['DB_id']


class table_Version(models.Model):
    '版本管理表'
    DB_id = models.BigAutoField(primary_key=True, null=False)
    允许的最低版本 = models.DecimalField(
        unique=True, max_digits=12, decimal_places=2, null=True)

    def __str__(self):
        return self.允许的最低版本

    class Meta:
        db_table = 'tabel_版本管理'
        verbose_name = '版本管理表'
        app_label = 'online'
        ordering = ['DB_id']


class table_Permission(models.Model):
    '版本管理表'
    DB_id = models.BigAutoField(primary_key=True, null=False)
    用户名 = models.CharField(max_length=255, null=False, unique=True)
    查看数据概览 = models.SmallIntegerField(null=True)
    查看单位信息 = models.SmallIntegerField(null=True)
    查看立项信息 = models.SmallIntegerField(null=True)
    查看招标信息 = models.SmallIntegerField(null=True)
    查看合同信息 = models.SmallIntegerField(null=True)
    查看预算信息 = models.SmallIntegerField(null=True)
    查看付款信息 = models.SmallIntegerField(null=True)
    查看变更信息 = models.SmallIntegerField(null=True)
    查看分包合同信息 = models.SmallIntegerField(null=True)
    操作单位信息 = models.SmallIntegerField(null=True)
    允许操作立项的项目 = models.CharField(max_length=255, null=True)
    允许操作招标的项目 = models.CharField(max_length=255, null=True)
    允许操作合同的项目 = models.CharField(max_length=255, null=True)
    操作预算信息 = models.SmallIntegerField(null=True)
    允许操作付款的项目 = models.CharField(max_length=255, null=True)
    允许操作变更的项目 = models.CharField(max_length=255, null=True)
    允许操作分包合同的项目 = models.CharField(max_length=255, null=True)
    允许调整概算的项目 = models.CharField(max_length=255, null=True)
    允许调整合同额的项目 = models.CharField(max_length=255, null=True)
    删除付款信息 = models.SmallIntegerField(null=True)

    def __str__(self):
        return self.用户名

    class Meta:
        db_table = 'tabel_权限信息'
        verbose_name = '权限信息表'
        app_label = 'online'
        ordering = ['DB_id']


class table_Company(models.Model):
    '单位信息表'
    单位识别码 = models.BigAutoField(primary_key=True, null=False)
    单位名称 = models.CharField(max_length=255, null=False, unique=True)
    单位类别 = models.CharField(max_length=255, null=True)
    单位性质 = models.CharField(max_length=255, null=True)
    法定代表人 = models.CharField(max_length=255, null=True)
    注册资金 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    单位资质 = models.CharField(max_length=255, null=True)
    银行账号 = models.CharField(max_length=255, null=True)
    联系人 = models.CharField(max_length=255, null=True)
    联系方式 = models.CharField(max_length=255, null=True)
    单位备注 = models.TextField(null=True)

    def __str__(self):
        return self.单位名称

    class Meta:
        unique_together = ('单位名称',)
        db_table = 'tabel_单位信息'
        verbose_name = '单位信息表'
        app_label = 'online'
        ordering = ['单位识别码']


class table_Initiation(models.Model):
    '立项信息表'
    立项识别码 = models.BigAutoField(primary_key=True, null=False)
    项目名称 = models.CharField(max_length=255, null=False)
    分项名称 = models.CharField(max_length=255, null=True)
    父项立项识别码 = models.BigIntegerField(null=True)
    建设单位识别码 = models.BigIntegerField(null=True)
    代建单位识别码 = models.BigIntegerField(null=True)
    立项文件名称 = models.CharField(max_length=255, null=True)
    立项简介 = models.TextField(null=True)
    立项时间 = models.DateField(null=True)
    项目概算 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    立项备注 = models.TextField(null=True)

    def __str__(self):
        return '{}-{}'.format(self.项目名称, self.分项名称)

    class Meta:
        unique_together = ('项目名称', '分项名称')
        db_table = 'tabel_立项信息'
        verbose_name = '立项信息表'
        app_label = 'online'
        ordering = ['立项识别码']


class table_Bidding(models.Model):
    '招标信息表'
    招标识别码 = models.BigAutoField(primary_key=True, null=False)
    立项识别码 = models.BigIntegerField(null=True)
    招标方式 = models.CharField(max_length=255, null=True)
    招标单位识别码 = models.BigIntegerField(null=True)
    招标代理识别码 = models.BigIntegerField(null=True)
    招标简介 = models.TextField(null=True)
    投标单位 = models.TextField(null=True)
    预算控制价 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    招标文件定稿时间 = models.DateField(null=True)
    公告邀请函发出时间 = models.DateField(null=True)
    开标时间 = models.DateField(null=True)
    中标通知书发出时间 = models.DateField(null=True)
    中标单位识别码 = models.BigIntegerField(null=True)
    中标价 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    招标备注 = models.TextField(null=True)

    def __str__(self):
        return '{}-{}'.format(self.招标方式, self.中标价)

    class Meta:
        db_table = 'tabel_招标信息'
        verbose_name = '招标信息表'
        app_label = 'online'
        ordering = ['招标识别码']


class table_Contract(models.Model):
    '合同信息表'
    合同识别码 = models.BigAutoField(primary_key=True, null=False)
    立项识别码 = models.BigIntegerField(null=True)
    招标识别码 = models.BigIntegerField(null=True)
    合同编号 = models.CharField(max_length=255, null=True,  unique=True)
    合同名称 = models.CharField(max_length=255, null=True)
    合同主要内容 = models.TextField(null=True)
    合同类别 = models.CharField(max_length=255, null=True)
    甲方识别码 = models.BigIntegerField(null=True)
    乙方识别码 = models.BigIntegerField(null=True)
    丙方识别码 = models.BigIntegerField(null=True)
    丁方识别码 = models.BigIntegerField(null=True)
    合同签订时间 = models.DateField(null=True)
    合同值_签订时 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    合同值_最新值 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    合同值_最终值 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    形象进度 = models.TextField(null=True)
    支付上限 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    开工时间 = models.DateField(null=True)
    竣工合格时间 = models.DateField(null=True)
    保修结束时间 = models.DateField(null=True)
    审计完成时间 = models.DateField(null=True)
    合同备注 = models.TextField(null=True)

    def __str__(self):
        return '{}-{}'.format(self.合同类别, self.合同名称)

    class Meta:
        db_table = 'tabel_合同信息'
        verbose_name = '合同信息表'
        app_label = 'online'
        ordering = ['合同识别码']


class table_Budget(models.Model):
    '预算信息表'
    预算识别码 = models.BigAutoField(primary_key=True, null=False)
    父项预算识别码 = models.BigIntegerField(null=True)
    预算名称 = models.CharField(max_length=255, null=True,  unique=True)
    预算周期 = models.CharField(max_length=255, null=True)
    预算总额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    预算备注 = models.TextField(null=True)

    def __str__(self):
        return '{}-{}'.format(self.预算名称, self.预算周期)

    class Meta:
        unique_together = ('预算名称', '预算周期')
        db_table = 'tabel_预算信息'
        verbose_name = '预算信息表'
        app_label = 'online'
        ordering = ['预算识别码']


class table_Payment(models.Model):
    '付款信息表'
    付款识别码 = models.BigAutoField(primary_key=True, null=False)
    付款登记时间 = models.DateField(null=True)
    付款支付时间 = models.DateField(null=True)
    立项识别码 = models.BigIntegerField(null=True)
    合同识别码 = models.BigIntegerField(null=True)
    付款事由 = models.TextField(null=True)
    付款单位识别码 = models.BigIntegerField(null=True)
    收款单位识别码 = models.BigIntegerField(null=True)
    预算识别码 = models.BigIntegerField(null=True)
    付款时预算总额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时项目概算 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时合同付款上限 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时合同值 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时预算余额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时概算余额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时合同可付余额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时合同未付额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时预算已付额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时合同已付额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时概算已付额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款时形象进度 = models.TextField(null=True)
    本次付款额 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    付款备注 = models.TextField(null=True)

    def __str__(self):
        return '{}-{}'.format(self.付款事由, self.本次付款额)

    class Meta:
        db_table = 'tabel_付款信息'
        verbose_name = '付款信息表'
        app_label = 'online'
        ordering = ['付款识别码']


class table_SubContract(models.Model):
    '分包合同信息表'
    分包合同识别码 = models.BigAutoField(primary_key=True, null=False)
    立项识别码 = models.BigIntegerField(null=True)
    合同识别码 = models.BigIntegerField(null=True)
    分包合同编号 = models.CharField(max_length=255, null=True,  unique=True)
    分包合同名称 = models.CharField(max_length=255, null=True)
    分包合同主要内容 = models.CharField(max_length=255, null=True)
    分包合同类别 = models.CharField(max_length=255, null=True)
    甲方识别码 = models.BigIntegerField(null=True)
    乙方识别码 = models.BigIntegerField(null=True)
    丙方识别码 = models.BigIntegerField(null=True)
    丁方识别码 = models.BigIntegerField(null=True)
    分包合同签订时间 = models.DateField(null=True)
    分包合同值_签订时 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    分包合同值_最新值 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    分包合同值_最终值 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    分包合同备注 = models.TextField(null=True)

    def __str__(self):
        return '{}-{}'.format(self.分包合同类别, self.分包合同名称)

    class Meta:
        db_table = 'tabel_分包合同信息'
        verbose_name = '分包合同信息表'
        app_label = 'online'
        ordering = ['分包合同识别码']


class table_Alteration(models.Model):
    '变更信息表'
    变更识别码 = models.BigAutoField(primary_key=True, null=False)
    立项识别码 = models.BigIntegerField(null=True)
    合同识别码 = models.BigIntegerField(null=True)
    变更类型 = models.CharField(max_length=255, null=True)
    变更编号 = models.CharField(max_length=255, null=True,  unique=True)
    变更主题 = models.CharField(max_length=255, null=True)
    变更登记日期 = models.DateField(null=True)
    变更生效日期 = models.DateField(null=True)
    变更原因 = models.TextField(null=True)
    预估变更额度 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    变更额度 = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    变更备注 = models.TextField(null=True)

    def __str__(self):
        return '{}-{}'.format(self.变更类型, self.变更主题)

    class Meta:
        db_table = 'tabel_变更信息'
        verbose_name = '变更信息表'
        app_label = 'online'
        ordering = ['变更识别码']
