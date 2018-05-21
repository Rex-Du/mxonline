from django.conf.urls import url, include

from users.views import LoginView, LogoutView, RegisterView, UserActiveView
from users.views import ForgetPwdView, ResetPwdView, ModifyPwdView, UserInfoView
from users.views import UploadImageView, UpdatePwdView, SendEmailView, ChangeEmailView, UserInfoUpdateView
from users.views import MyCourseView, MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='user_login'),
    url(r'^logout/$', LogoutView.as_view(), name='user_logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name='forgetpwd'),
    url(r'^active/(?P<code>.*)/$', UserActiveView.as_view(), name='active'),
    url(r'^reset/(?P<code>.*)/$', ResetPwdView.as_view(), name='reset'),
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify'),
    url(r'^captcha/', include('captcha.urls')),
    # 个人中心
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 个人中心修改头像
    url(r'^image/$', UploadImageView.as_view(), name='user_image'),
    # 个人中心修改密码
    url(r'^changepwd/$', UpdatePwdView.as_view(), name='user_change_pwd'),
    # 个人中心修改邮箱发送邮箱验证码
    url(r'^send_email/$', SendEmailView.as_view(), name='send_email'),
    # 个人中心修改邮箱
    url(r'^change_eamil/$', ChangeEmailView.as_view(), name='change_email'),
    # 个人中心修改信息保存
    url(r'^update_info/$', UserInfoUpdateView.as_view(), name='update_info'),
    # 个人中心我的课程
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),
    # 个人中心我的收藏-授课机构
    url(r'^my_fav_org/$', MyFavOrgView.as_view(), name='my_fav_org'),
    # 个人中心我的收藏-授课讲师
    url(r'^my_fav_teacher/$', MyFavTeacherView.as_view(), name='my_fav_teacher'),
    # 个人中心我的收藏-课程
    url(r'^my_fav_course/$', MyFavCourseView.as_view(), name='my_fav_course'),
    # 个人中心我的消息
    url(r'^my_message/$', MyMessageView.as_view(), name='my_message'),
]