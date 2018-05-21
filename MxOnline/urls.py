"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from MxOnline.settings import MEDIA_ROOT # STATIC_ROOT
import xadmin
from django.views.static import serve
from django.views.generic import TemplateView
from users.views import HomePageView


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    # 直接显示页面的url配置
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^chart$', TemplateView.as_view(template_name='chart.html'), name='chart'),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^user/', include('users.urls')),
    url(r'^org/', include('organization.urls')),
    url(r'^course/', include('courses.urls')),
    url(r'^operta/', include('operation.urls')),
    # 配置上传文件的访问方法
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # 当debug=false时，static失效了，所以要加以下配置
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT})
    url(r'^ueditor/',include('DjangoUeditor.urls' ))
]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'