from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger  # 安装的是django-pure_pagination第三方模块
from django.http import HttpResponse
from django.db.models import Q

from organization.models import *
from courses.models import *
from operation.models import *
# Create your views here.


class OrgListView(View):
    """
    机构列表显示的view
    """
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        city_id = request.GET.get('city', '')

        # 机构搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords)
                                             | Q(desc__icontains=keywords))
        # 筛选功能
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)
        ct = request.GET.get('ct', '')
        if ct:
            all_orgs = all_orgs.filter(category=ct)
        sort_by = request.GET.get('sort', '')
        if sort_by:
            all_orgs = all_orgs.order_by(sort_by)

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 4, request=request)
        orgs_per_page = p.page(page)

        org_num = all_orgs.count()

        all_citys = CityDict.objects.all()

        best_orgs = CourseOrg.objects.all().order_by('-fav_nums')[0:3]
        return render(request, 'org-list.html', {
            'orgs_per_page': orgs_per_page,
            'all_citys': all_citys,
            'org_num': org_num,
            'city_id': city_id,
            'ct': ct,
            'best_orgs': best_orgs,
            'sort_by': sort_by
        })


class OrgDetailView(View):
    def get(self, request):
        org_id = int(request.GET.get('org-id', ''))
        try:
            org = CourseOrg.objects.get(id=org_id)
            org.click_nums += 1
            org.save()
        except Exception as e:
            org = ''
        org_courses = Course.objects.filter(course_org_id=org_id)
        org_teachers = Teacher.objects.filter(org_id=org_id)
        url = request.path.split('/')[2]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorate.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_fav = True
        if url == 'org-home':
            return render(request, 'org-detail-homepage.html',{
                          'org': org,
                          'org_courses': org_courses,
                          'org_teachers': org_teachers,
                          'url': url,
                          'has_fav': has_fav
                    })
        elif url == 'org-course':
            return render(request, 'org-detail-course.html',{
                          'org': org,
                          'org_courses': org_courses,
                          'url': url,
                          'has_fav': has_fav
                    })
        elif url == 'org-desc':
            return render(request, 'org-detail-desc.html', {
                            'org': org,
                            'url': url,
                            'has_fav': has_fav
                    })
        elif url == 'org-teacher':
            return render(request, 'org-detail-teachers.html', {
                            'org': org,
                            'org_teachers': org_teachers,
                            'url': url,
                            'has_fav': has_fav
                    })


class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        user = request.user
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        fav_exit = UserFavorate.objects.filter(user=user, fav_id=int(fav_id), fav_type=int(fav_type))

        # 如果该用户已收藏过，则取消收藏
        if fav_exit:
            fav_exit.delete()
            # 取消收藏之后，对应的被收藏主体的收藏数减1
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else: # 如果该用户没有收藏过，则收藏
            userfav = UserFavorate()
            userfav.user = user
            userfav.fav_id = int(fav_id)
            userfav.fav_type = int(fav_type)
            userfav.save()
            # 收藏之后，对应的被收藏主体的收藏数加1
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums += 1
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                print(org.fav_nums)
                org.fav_nums += 1
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums += 1
                teacher.save()
        return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()

        # 机构搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            teachers = teachers.filter(Q(name__icontains=keywords))

        # 排序功能
        sort_by = request.GET.get('sort', '')
        if sort_by:
            teachers = teachers.order_by('-fav_nums')
        # 讲师排行榜
        best_teachers = teachers.order_by('-fav_nums')[:2]

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 4, request=request)
        teachers_per_page = p.page(page)
        return render(request, 'teachers-list.html', {'teachers_per_page': teachers_per_page, 'sort_by': sort_by,
                                                      'best_teachers': best_teachers})


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        courses = Course.objects.filter(teacher=teacher)
        teacher.click_nums += 1
        # 是否收藏了讲师
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorate.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True
            if UserFavorate.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True
        # 讲师排行榜
        best_teachers = Teacher.objects.all().order_by('-fav_nums')[:2]
        return render(request, 'teacher-detail.html', {'teacher': teacher, 'courses': courses,
               'has_fav_teacher': has_fav_teacher, 'has_fav_org': has_fav_org, 'best_teachers': best_teachers})