from datetime import datetime

from django.db import models

# Create your models here.


class CityDict(models.Model):
    name = models.CharField('城市名', max_length=30)
    desc = models.CharField('描述', max_length=50)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField('机构名', max_length=40)
    category = models.CharField('机构类别', max_length=4, choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')), default='pxjg')
    desc = models.CharField('描述', max_length=100)
    click_nums = models.IntegerField('点击量', default=0)
    fav_nums = models.IntegerField('收藏量', default=0)
    image = models.ImageField('封面图', upload_to='org/%Y/%m')
    address = models.CharField('机构地址', max_length=100)
    city = models.ForeignKey(CityDict, verbose_name='城市')
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    students = models.IntegerField('学生数量', default=0)
    courses = models.IntegerField('课程数', default=0)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='所属机构', )
    name = models.CharField('教师名', max_length=40)
    work_years = models.IntegerField('工作年限', default=0)
    work_company = models.CharField('就职公司', max_length=40)
    work_position = models.CharField('职位', max_length=40)
    points = models.CharField('教学特点', max_length=100)
    click_nums = models.IntegerField('点击量', default=0)
    fav_nums = models.IntegerField('收藏量', default=0)
    add_time = models.DateTimeField('添加时间', default=datetime.now)
    img = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='老师头像', null=True)
    age = models.IntegerField('年龄', default=30, null=True)
    level = models.CharField('级别', max_length=4, choices=(('JPJS', '金牌讲师'), ('YPJS', '银牌讲师'), ('TPJS', '铜牌讲师')), default='YPJS')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name