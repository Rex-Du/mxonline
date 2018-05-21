from django.conf.urls import url

from courses.views import CoursesListView, CoursesDetailView, CoursesInfoView, CoursesCommentView, AddCommentView,\
    CoursesVideoView, UserCourseView

"""
    这里的url得注意，不能用.*，因为图片资源的url是加在原始url之后的，如果写成.*，
    请求图片地址是会报错
"""

urlpatterns = [
    url(r'^list/$', CoursesListView.as_view(), name='courses-list'),
    # url(r'^detail/(?P<course_id>.*)/$', CoursesDetailView.as_view(), name='courses-detail'),
    url(r'^detail/(?P<course_id>\d+)/$', CoursesDetailView.as_view(), name='courses-detail'),
    url(r'^info/(?P<course_id>\d+)/$', CoursesInfoView.as_view(), name='courses-info'),
    url(r'^video/(?P<video_id>\d+)/$', CoursesVideoView.as_view(), name='courses-video'),
    url(r'^comment/(?P<course_id>\d+)/$', CoursesCommentView.as_view(), name='courses-comment'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add-comment'),
    url(r'^sign_up/$', UserCourseView.as_view(), name='sign-up'),
]