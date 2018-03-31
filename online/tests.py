from django.test import TestCase
from online.views.offical import *

# Create your tests here.

# python manage.py test online.tests --keepdb


class permission_API_TestCase(TestCase):

    def setUp(self):
        '''
            excute before test.
        '''
        print("Permission API will be tested. Now, Let's ride!")

    def tearDown(self):
        '''
            excute after test.
        '''
        print("Permission API has been tested.")

    def test_can_Write_Table(self):
        test_datas = [
            # username = guxiang
            # classify = 单位
            [['guxiang', ['单位']],                        True],
            # classify = 立项
            [['guxiang', ['立项', '北王安置房']],           True],
            [['guxiang', ['立项', '南王安置房']],           True],
            [['guxiang', ['立项', '天水路派出所']],         True],
            [['guxiang', ['立项', '天水路交警队']],         False],
            [['guxiang', ['立项', '北王其他费用']],          True],
            [['guxiang', ['立项', '1609工程']],            True],
            [['guxiang', ['立项', '1609工程其他']],         True],
            [['guxiang', ['立项', '']],                    False],
            # classify = 招标
            [['guxiang', ['招标', '北王安置房']],           True],
            [['guxiang', ['招标', '南王安置房']],           True],
            [['guxiang', ['招标', '天水路派出所']],         True],
            [['guxiang', ['招标', '天水路交警队']],         False],
            [['guxiang', ['招标', '北王其他费用']],          True],
            [['guxiang', ['招标', '1609工程']],            True],
            [['guxiang', ['招标', '1609工程其他']],         True],
            # classify = 合同
            [['guxiang', ['合同', '北王安置房']],           True],
            [['guxiang', ['合同', '南王安置房']],           True],
            [['guxiang', ['合同', '天水路派出所']],         True],
            [['guxiang', ['合同', '天水路交警队']],         False],
            [['guxiang', ['合同', '北王其他费用']],          True],
            [['guxiang', ['合同', '1609工程']],            True],
            [['guxiang', ['合同', '1609工程其他']],         True],
            # classify = 招标
            [['guxiang', ['招标', '北王安置房']],           True],
            [['guxiang', ['招标', '南王安置房']],           True],
            [['guxiang', ['招标', '天水路派出所']],         True],
            [['guxiang', ['招标', '天水路交警队']],         False],
            [['guxiang', ['招标', '北王其他费用']],          True],
            [['guxiang', ['招标', '1609工程']],            True],
            [['guxiang', ['招标', '1609工程其他']],         True],
            # classify = 预算
            [['guxiang', ['预算']],                         True],
            # classify = 变更
            [['guxiang', ['变更', '北王安置房']],           True],
            [['guxiang', ['变更', '南王安置房']],           True],
            [['guxiang', ['变更', '天水路派出所']],         True],
            [['guxiang', ['变更', '天水路交警队']],         False],
            [['guxiang', ['变更', '北王其他费用']],          True],
            [['guxiang', ['变更', '1609工程']],            True],
            [['guxiang', ['变更', '1609工程其他']],         True],
            # classify = 付款
            [['guxiang', ['付款', '北王安置房']],           True],
            [['guxiang', ['付款', '南王安置房']],           True],
            [['guxiang', ['付款', '天水路派出所']],         True],
            [['guxiang', ['付款', '天水路交警队']],         False],
            [['guxiang', ['付款', '北王其他费用']],          True],
            [['guxiang', ['付款', '1609工程']],            True],
            [['guxiang', ['付款', '1609工程其他']],         True],
            # classify = 分包合同
            [['guxiang', ['分包合同', '北王安置房']],           True],
            [['guxiang', ['分包合同', '南王安置房']],           True],
            [['guxiang', ['分包合同', '天水路派出所']],         True],
            [['guxiang', ['分包合同', '天水路交警队']],         False],
            [['guxiang', ['分包合同', '北王其他费用']],          True],
            [['guxiang', ['分包合同', '1609工程']],            True],
            [['guxiang', ['分包合同', '1609工程其他']],         True],
            # classify = 概算
            [['guxiang', ['概算', '北王安置房']],           True],
            [['guxiang', ['概算', '南王安置房']],           True],
            [['guxiang', ['概算', '天水路派出所']],         True],
            [['guxiang', ['概算', '天水路交警队']],         False],
            [['guxiang', ['概算', '北王其他费用']],          True],
            [['guxiang', ['概算', '1609工程']],            True],
            [['guxiang', ['概算', '1609工程其他']],         True],
            # classify = 合同额
            [['guxiang', ['合同额', '北王安置房']],           True],
            [['guxiang', ['合同额', '南王安置房']],           True],
            [['guxiang', ['合同额', '天水路派出所']],         True],
            [['guxiang', ['合同额', '天水路交警队']],         False],
            [['guxiang', ['合同额', '北王其他费用']],          True],
            [['guxiang', ['合同额', '1609工程']],            True],
            [['guxiang', ['合同额', '1609工程其他']],         True],
        ]
        i = 0
        for element in test_datas:
            i += 1
            print('现在正在测试can_Write_Table方法的第%d组数据...' % i)
            username, arguments = element[0]
            value = getUserPermission(username).can_Write_Table(*arguments)
            print('输入值为：<%s>, <%s>' % (username, arguments))
            print('输出值为：<%s>' % value)
            self.assertEqual(value, element[1])