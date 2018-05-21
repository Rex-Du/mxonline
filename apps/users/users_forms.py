# encoding : utf-8
# author   : DQ 
# creattime: 2017-07-19 16:58
from django import forms
from captcha.fields import CaptchaField     # 这里安装的是django-simple-captcha这个第三方库，而不是capthca
from django.forms import ModelForm

from users.models import UserProfile


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=6)
    captcha = CaptchaField()


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(min_length=6)
    password2 = forms.CharField(min_length=6)


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class UserUploadImageForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']
