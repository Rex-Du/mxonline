# encoding : utf-8
# author   : DQ 
# creattime: 2017-07-19 10:34
import xadmin

from organization.models import *


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'category', 'desc', 'add_time', 'click_nums', 'address', 'city']
    search_fields =  ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time', 'click_nums', 'address']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'add_time', 'work_company', 'work_years']
    search_fields =  ['org', 'name', 'work_company', 'work_years']
    list_filter = ['org', 'name', 'add_time', 'work_company', 'work_years']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
