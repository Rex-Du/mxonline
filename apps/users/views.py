import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.base_user import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 安装的是django-pure_pagination第三方模块

from users.models import UserProfile, EmailVerifyRecord, Banner
from users.users_forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, UserInfoUpdateForm
from utils.send_email import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from users.users_forms import UserUploadImageForm
from operation.models import UserCourse
from operation.models import  UserFavorate, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from django.core.management import execute_from_command_line

# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            password = request.POST.get('password', '')

            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html',
                              {'msg': '邮箱已被使用，请更换邮箱重试！', 'register_form': register_form})

            send_register_email(username, 'register')
            newuser = UserProfile()
            newuser.username = username
            newuser.email = username
            newuser.password = make_password(password)
            newuser.is_active = False
            newuser.save()
            return redirect('/user/login/')
            # return render(request, 'login.html', {'msg': '注册成功，激活邮件已发送到您的注册邮箱，请激活后登录！'})
        return render(request, 'register.html', {'register_form': register_form})


class UserActiveView(View):
    def get(self, request, code):
        email_verify_record = EmailVerifyRecord.objects.filter(code=code)
        if email_verify_record:
            for each_email in email_verify_record:
                user = UserProfile.objects.get(email=each_email.email)
                if user.is_active:
                    pass
                else:
                    user.is_active = True
                    user.save()
        return redirect('/user/login/')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                status = send_register_email(email, 'forget')
                if status:
                    return render(request, 'sendsccess.html')
                else:
                    return render(request, 'sendfail.html')
            else:
                return render(request, 'forgetpwd.html',
                              {'msg': '邮箱未注册，请检查邮箱地址是否正确!', 'forget_form': forget_form})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetPwdView(View):
    def get(self, request, code):
        try:
            email_verify_record = EmailVerifyRecord.objects.get(code=code, send_type='forget')
        except :
            email_verify_record = False
        if email_verify_record:
            return render(request, 'password_reset.html', {'email': email_verify_record.email})
        return render(request, 'resetfail.html')


class ModifyPwdView(View):
    '''
    自己多做了一步，当用用户手动修改了email地址之后，拦截下来，提示链接失效
    '''
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '密码输入不一致'})
            else:
                email = request.POST.get('email', '')
                email_verify_record = EmailVerifyRecord.objects.filter(email=email, send_type='forget')
                if email_verify_record:
                    user = UserProfile.objects.get(email=email)
                    user.password = make_password(pwd2)
                    user.save()
                    email_verify_record.delete()
                    return redirect('/login/')
                else:
                    return render(request, 'password_reset.html',
                                  {'msg': '重置密码失败或链接失效！', 'email': email})
        else:
            return render(request, 'password_reset.html', {'modify_form': modify_form})


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    '''
    # 类方式的用户登录认证，代替了下面的user_login方法
    '''

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)        # 这里传的是request.POST，否则就会报错的
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    # return render(request, 'index.html')
                    return HttpResponseRedirect(reverse('home'))
                return render(request, 'login.html', {'msg': '用户未激活！'})
            return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('home'))

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误！'})
#     elif request.method == 'GET':
#         return render(request, 'login.html')
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {})


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        user_image = UserUploadImageForm(request.POST, request.FILES, instance=request.user)
        if user_image.is_valid():
            user_image.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    '''
    自己多做了一步，当用用户手动修改了email地址之后，拦截下来，提示链接失效
    '''
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailView(View):
    def post(self, request):
        email_addr = request.POST.get('email', '')
        if not email_addr:
            return HttpResponse('{"email":"邮件地址不空为空"}', content_type='application/json')
        if UserProfile.objects.filter(email=email_addr):
            return HttpResponse('{"email":"你输入的邮箱地址已被其它账号使用！"}', content_type='application/json')
        status = send_register_email(email_addr, 'changeemail')
        if status:
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class ChangeEmailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        email_verify_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='changeemail')
        if email_verify_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"邮箱或验证码错误，请确认！"}', content_type='application/json')


class UserInfoUpdateView(View):
    def post(self, request):
        user_info = UserInfoUpdateForm(request.POST, instance=request.user)
        if user_info.is_valid():
            user_info.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info.errors), content_type='application/json')


class MyCourseView(View):
    def get(self, request):
        my_courses = UserCourse.objects.filter(user=request.user)
        courses_list = []
        for my_course in my_courses:
            course = Course.objects.get(id=my_course.course_id)
            courses_list.append(course)
        return render(request, 'usercenter-mycourse.html', {'courses_list': courses_list})


class MyFavOrgView(View):
    def get(self, request):
        my_fav_orgs = UserFavorate.objects.filter(user=request.user, fav_type=2)
        my_fav_orgs_list = []
        for my_fav_org in my_fav_orgs:
            org = CourseOrg.objects.get(id=my_fav_org.fav_id)
            my_fav_orgs_list.append(org)
        return render(request, 'usercenter-fav-org.html', {'my_fav_orgs_list': my_fav_orgs_list})


class MyFavTeacherView(View):
    def get(self, request):
        my_fav_teachers = UserFavorate.objects.filter(user=request.user, fav_type=3)
        my_fav_teachers_list = []
        for my_fav_teacher in my_fav_teachers:
            teacher = Teacher.objects.get(id=my_fav_teacher.fav_id)
            my_fav_teachers_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {'my_fav_teachers_list': my_fav_teachers_list})


class MyFavCourseView(View):
    def get(self, request):
        my_fav_courses = UserFavorate.objects.filter(user=request.user, fav_type=1)
        my_fav_courses_list = []
        for my_fav_course in my_fav_courses:
            course = Course.objects.get(id=my_fav_course.fav_id)
            my_fav_courses_list.append(course)
        return render(request, 'usercenter-fav-course.html', {'my_fav_courses_list': my_fav_courses_list})


class MyMessageView(View):
    def get(self, request):
        messages = UserMessage.objects.filter(user=request.user.id).order_by('has_read')
        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, 2, request=request)
        messages = p.page(page)
        for message in messages.object_list:
            message.has_read = 1
            message.save()
        return render(request, 'usercenter-message.html', {'messages': messages})


class HomePageView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        banner_courses = Course.objects.filter(is_banner=True)
        courses = Course.objects.filter(is_banner=False)[:6]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {'all_banners': all_banners,
                                              'banner_courses': banner_courses, 'courses': courses,
                                              'orgs': orgs})


def page_not_found(request):
    # 全局404页面配置
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_not_found(request):
    # 全局500页面配置
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response