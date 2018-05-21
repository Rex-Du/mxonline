# Author   : Jim-Du 
# CreateTime: 2017-07-30


from django.conf.urls import url, include

from operation.views import UserAskView


urlpatterns = [
    url(r'^userask/$', UserAskView.as_view(), name='userask'),

]