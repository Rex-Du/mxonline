from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from courses.models import *
from operation.models import CourseComments, UserCourse, UserFavorate
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CoursesListView(View):
    """
    课程列表页
    """
    def get(self, request):
        all_courses = Course.objects.all().order_by('add_time')

        # 课程搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)
                                             |Q(desc__icontains=keywords)
                                             |Q(detail__icontains=keywords))
        sort_by = request.GET.get('sort', '')
        if sort_by:
            all_courses = all_courses.order_by(sort_by)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)
        courses_per_page = p.page(page)
        return render(request, 'course-list.html', locals())


class CoursesDetailView(View):
    """
    课程详情页面
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        related_courses = Course.objects.filter(course_org=course.course_org).exclude(id=course.id)
        course.click_nums += 1
        course.save()
        print(related_courses)
        # 是否已报名
        has_enroll = False
        # 是否收藏了该课程对应的机构
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorate.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav = True
            if UserCourse.objects.filter(user=request.user, course=course.id):
                has_enroll = True
        return render(request, 'course-detail.html', {'course': course, 'has_enroll': has_enroll,
                                    'has_fav': has_fav, 'related_courses': related_courses})


class UserCourseView(View):
    """
    用户报名，用户取消报名
    """
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        user = request.user
        course = request.POST.get('course', 0)
        fav_exit = UserCourse.objects.filter(user=user, course_id=int(course))

        # 如果该用户已报名，则取消报名
        if fav_exit:
            fav_exit.delete()
            # 取消报名之后，对应的课程学生数减1
            course = Course.objects.get(id=int(course))
            course.students -= 1
            course.save()
            return HttpResponse('{"status":"success", "msg":"报名"}', content_type='application/json')
        else: # 如果该用户没有报名过，则报名
            # 报名之后，对应的课程学生数加1
            course = Course.objects.get(id=int(course))
            course.students += 1
            course.save()

            user_course = UserCourse()
            user_course.user = user
            user_course.course = course
            user_course.save()

        return HttpResponse('{"status":"success", "msg":"已报名"}', content_type='application/json')


class CoursesInfoView(LoginRequiredMixin, View):
    """
    课程学习页面
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        lessons = Lesson.objects.filter(course=course)


        # 点击‘开始学习’后，将学生与该课程关联上
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        # if not user_course:
        #     user_course = UserCourse(user=request.user, course=course)
        #     user_course.save()
        # 学过这个课程的学生还学过哪些课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user.user.id for user in user_courses]
        courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [course.course.id for course in courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        if len(related_courses)>3:
            related_courses = related_courses[:3]
        return render(request, 'course-video.html', {'course': course,
                    'lessons': lessons, 'related_courses': related_courses})


class CoursesVideoView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        lessons = Lesson.objects.filter(course=course)

        # 点击‘开始学习’后，将学生与该课程关联上
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 学过这个课程的学生还学过哪些课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user.user.id for user in user_courses]
        courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [course.course.id for course in courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        if len(related_courses)>3:
            related_courses = related_courses[:3]
        return render(request, 'course-play.html', {'course': course, 'lessons': lessons,
                                                     'related_courses': related_courses, 'video': video})


class CoursesCommentView(LoginRequiredMixin, View):
    """
    课程评论页面
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        lessons = Lesson.objects.filter(course=course)
        comments = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {'course': course, 'lessons': lessons, 'comments': comments})


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        course_id = int(request.POST.get('course_id', '0'))
        comment = request.POST.get('comments', '')
        if course_id>0 and comment:
            course_comment = CourseComments()
            course = Course.objects.get(id=course_id)
            course_comment.course = course
            course_comment.user = request.user
            course_comment.comments = comment
            course_comment.save()
            return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')