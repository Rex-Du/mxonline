from django.conf.urls import url, include

from organization.views import OrgListView, OrgDetailView, AddFavView, TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgListView.as_view(), name='org-list'),
    url(r'^org-home/$', OrgDetailView.as_view(), name='org-home'),
    url(r'^org-course/$', OrgDetailView.as_view(), name='org-course'),
    url(r'^org-desc/$', OrgDetailView.as_view(), name='org-desc'),
    url(r'^org-teacher/$', OrgDetailView.as_view(), name='org-teacher'),
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    url(r'^teacher/$', TeacherListView.as_view(), name='teacher'),
    url(r'^teacher-detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher-detail'),
]