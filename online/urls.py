from django.conf.urls import url
from online.views import views, v_table, offical

urlpatterns = [
    # ------------------------------------以下为正式系统URL----------------------------------------

    # 登陆界面
    url(r'^$',                            offical.login,
        name='login'),
    # 注销
    url(r'^logout/$',                     offical.logout,
        name='logout'),

    # 主界面
    url(r'^overview/$',                   offical.overview,
        name='overview'),

    # 图表界面
    url(r'^big_Pie/$',                    offical.big_Pie,
        name='big_Pie'),

    # 表格界面
    url(r'^tableFrame/(\w*/*)$',
        offical.tableFrame,              name='tableFrame'),

    # 选择器界面
    url(r'^inputer_table/(\w*/*)$',
        offical.inputer_table,           name='inputer_table'),

    # 表单群界面
    url(r'^inputFrame/(\w*/*)$',
        offical.inputFrame,              name='inputFrame'),

    # 附件界面
    url(r'^attachFrame/(\w*/*)$',
        offical.attachFrame,             name='attachFrame'),

    # 输入表单界面
    url(r'^inputer/(\w*/*)$',
        offical.inputer,                 name='inputer'),

    # 输入上传界面
    url(r'^uploader/$',
        offical.uploader,                name='uploader'),

    # ajax
    url(r'ajax_table_data',               offical.ajax_table_data,
        name='ajax_table_data'),

    url(r'ajax_tree_data',                offical.ajax_tree_data,
        name='ajax_tree_data'),

    url(r'ajax_treeTable',                offical.ajax_treeTable,
        name='ajax_treeTable'),

    url(r'getDataForOverview',            offical.getDataForOverview,
        name='getDataForOverview'),

    url(r'get_Pie_Data',                  offical.get_Pie_Data,
        name='get_Pie_Data'),

    url(r'list_file',                     offical.list_file,
        name='list_file'),

    url(r'get_file_url',                  offical.get_file_url,
        name='get_file_url'),

    url(r'get_file_upload_passwords',     offical.get_file_upload_passwords,
        name='get_file_upload_passwords'),

    url(r'get_Write_Permission',          offical.get_Write_Permission,
        name='get_Write_Permission'),

    url(r'get_WritePermissionObj',        offical.get_WritePermissionObj,
        name='get_WritePermissionObj'),

    url(r'ajax_save_data',                offical.ajax_save_data,
        name='ajax_save_data'),

    url(r'ajax_del_data',                 offical.ajax_del_data,
        name='ajax_del_data'),



]
