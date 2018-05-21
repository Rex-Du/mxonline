# encoding : utf-8
# author   : DQ 
# creattime: 2017-07-19 10:06
from courses.models import *
# from organization.models import CourseOrg

import xadmin


class LessonInline(object):     # 这步是让xadmin中添加课程时可以同时在下面添加章节
    model = Lesson
    extra = 0


class CourseResourceShow(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'degree', 'add_time']
    search_fields = ['name', 'desc', 'degree']
    list_filter = ['name', 'desc', 'degree', 'add_time']
    inlines = [LessonInline, CourseResourceShow]

    def save_models(self):
        # 在添加了新的课程之后，给课程机构中的课程数量加1
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            # 下面这步没有直接加1，因为课程有可能是加也有可能是减，不管如何都重新统计再保存是没问题的
            course_org.courses = Course.objects.filter(course_org=course_org).count()
            course_org.save()

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lession', 'name', 'add_time']
    search_fields = ['lession', 'name']
    list_filter = ['lession__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
