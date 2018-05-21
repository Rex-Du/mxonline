from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField('昵称',max_length=50, default='')
    birday = models.DateField('生日', null=True, blank=True)
    gender = models.CharField('性别', choices=(('male','男'),('female','女')),default='male', max_length=6)
    address = models.CharField('地址', max_length=80, default='')
    mobile = models.CharField('手机号', max_length=11, null=True, blank=True)
    image = models.ImageField('头像', upload_to='image/%Y/%m', default='image/default.png')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):    # 用来定义表在后台admin中的显示方式，这里表示显示name字段
        return self.username

    def get_user_messages(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=0).count()


class EmailVerifyRecord(models.Model):
    # 用于存放验证码信息的表
    code = models.CharField('验证码', max_length=10)
    email = models.EmailField('邮箱地址', max_length=50)
    send_type = models.CharField('发送方式', choices=(('register', '注册'), ('forget', '忘记密码'), ('changeeamil', '更换邮箱')), max_length=15)
    send_time = models.DateTimeField('发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email


class Banner(models.Model):
    # 用于存放轮播图信息的表
    title = models.CharField('标题', max_length=100)
    image = models.ImageField('图片', upload_to='banner/%Y/%m', max_length=100)
    url = models.URLField('访问地址', max_length=200)
    index = models.IntegerField('顺序', default=100)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name