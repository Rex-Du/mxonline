from datetime import datetime

from django.db import models

from users.models import UserProfile
from courses.models import Course
# Create your models here.


class UserAsk(models.Model):
    name = models.CharField('姓名', max_length=40)
    mobile = models.CharField('手机号', max_length=11)
    course_name = models.CharField('课程名', max_length=50)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    comments = models.CharField('评论', max_length=200)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorate(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField('数据id', default=0)             # 直接是收藏对象的id，使用时与fav_type字段一起得出结果
    fav_type = models.IntegerField('收藏类型', choices=((1,'课程'), (2, '课程机构'), (3, '讲师')), default=1)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


# class UserSignUp(models.Model):
#     user = models.ForeignKey(UserProfile, verbose_name='用户')
#     course = models.ForeignKey(Course, verbose_name='课程')            # 直接是收藏对象的id，使用时与fav_type字段一起得出结果
#     add_time = models.DateTimeField('添加时间', default=datetime.now)
#
#     class Meta:
#         verbose_name = '用户报名'
#         verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField('接收用户', default=0)      # 指定接收消息的用户，为0是发给所有用户，不为0时直接指定用户的id
    message = models.CharField('消息内容', max_length=400)
    has_read = models.BooleanField('是否已读', default=False)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name