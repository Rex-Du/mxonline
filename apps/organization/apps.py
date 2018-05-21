from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    name = 'organization'
    verbose_name = '机构'     # 修改后台管理页面中左边菜单为中文，与init.py中的default_app_config一起用才能生效
