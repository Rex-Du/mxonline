# encoding : utf-8
# author   : DQ 
# creattime: 2017-07-19 09:21
from django.contrib import admin

import xadmin
from xadmin import views

from users.models import EmailVerifyRecord, Banner


class BaseSettings(object):     # 给后台管理系统加上换主题的功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):   # 修改后台管理系统标题和页脚， 将菜单弄成折叠的
    site_title = '流水在线后台管理'
    site_footer = '流水在线学习网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type']   # 定义后台管理中表显示的字段，顺序与这里写的一致
    search_fields = ['code', 'email', 'send_type']  # 定义后台管理中搜索时的字段，顺序与这里写的一致
    list_filter = ['code', 'email', 'send_type', 'send_time']     # 定义后台管理中过滤时的字段


class BannerAdmin(object):
    list_display = ['title', 'image', 'url']
    search_fields = ['title', 'image', 'url']
    list_filter = ['title', 'image', 'url']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)