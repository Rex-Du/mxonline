from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField

from organization.models import CourseOrg, Teacher
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(verbose_name='课程机构', to=CourseOrg)
    name = models.CharField('课程名称', max_length=100)
    is_banner = models.BooleanField('是否轮播图', default=False)
    desc = UEditorField('课程简介', width=600, height=300, toolbars="full",
                        imagePath="course/", filePath="course/")
    detail = models.TextField('课程详情')
    degree = models.CharField('课程难度', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')),max_length=2)
    learn_times = models.IntegerField('学习时长(分钟数)', default=0)
    students = models.IntegerField('学习人数', default=0)
    fav_nums = models.IntegerField('收藏人数', default=0)
    image = models.ImageField('封面图', upload_to='course/%Y/%m')
    click_nums = models.IntegerField('点击量', default=0)
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    category = models.CharField('课程分类', max_length=100)
    teacher = models.ForeignKey(verbose_name='讲师', to=Teacher, null=True)
    you_need_know = models.CharField('你需要知道', default='人要没决心，一事无成！', max_length=1000)
    teacher_say = models.CharField('老师带话', default='学习改变命运', max_length=300)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_resources(self):
        return self.courseresource_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField('章节名', max_length=50)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField('视频名称', max_length=50)
    url = models.CharField('播放地址', max_length=500, default='')
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField('名称', max_length=50)
    download = models.FileField('下载地址', upload_to='course/resource/%Y/%m', max_length=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
