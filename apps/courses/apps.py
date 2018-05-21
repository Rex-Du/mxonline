from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'courses'
    verbose_name = '课程'     # 修改后台管理页面中左边菜单为中文，与init.py中的default_app_config一起用才能生效
