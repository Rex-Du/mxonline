from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户'     # 修改后台管理页面中左边菜单为中文，与init.py中的default_app_config一起用才能生效
