from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from courses import forms, models
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class CreateCourseView(UserPassesTestMixin, CreateView):
    model = models.Course
    form_class = forms.CourseForm
    template_name = 'courses/course-form.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'pk': self.object.pk})

class UpdateCourseView(UserPassesTestMixin, UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    template_name = 'courses/course-form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user in self.get_object().teachers.all()

    def get_success_url(self):
        return reverse('courses:detail', kwargs={'pk': self.object.pk})

class CreateChapterView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, course_id):
        course = get_object_or_404(models.Course, id=course_id)
        form = forms.CourseChapterForm(request.POST, request.FILES)
        if form.is_valid():
            new_course_chapter = models.CourseChapter(
                title = form.cleaned_data['title'],
                number = form.cleaned_data['number'],
                course = course
            )
            new_course_chapter.save()

        return HttpResponseRedirect(reverse('courses:lessons', kwargs = {'pk': course.pk}))

class UpdateChapterView(UserPassesTestMixin, UpdateView):
    model = models.CourseChapter
    form_class = forms.CourseChapterForm

    def test_func(self):
        return self.request.user.is_superuser or self.request.user in self.get_object().course.teachers.all()

    def get_success_url(self):
        return reverse('courses:lessons', kwargs={'pk': self.object.course.pk})

class CreateLessonView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, chapter_id):
        course_chapter = get_object_or_404(models.CourseChapter, id=chapter_id)
        form = forms.LessonForm(request.POST, request.FILES)
        if form.is_valid():
            new_lesson = models.Lesson(
                title = form.cleaned_data['title'],
                number = form.cleaned_data['number'],
                chapter = course_chapter,
                estimated_time_min = form.cleaned_data['estimated_time_min'],
                description = form.cleaned_data['description']
            )
            new_lesson.save()
            new_homework = models.Homework(
                lesson = new_lesson,
                text = 'Текст домашнего задания',
                points = 10
            )
            new_homework.save()
            return HttpResponseRedirect(reverse('courses:lessons', kwargs = {'pk': course_chapter.course.pk})+f'?lesson_id={new_lesson.id}')
        
        return HttpResponseRedirect(reverse('courses:lessons', kwargs = {'pk': course_chapter.course.pk}))

class UpdateLessonView(UserPassesTestMixin, UpdateView):
    model = models.Lesson
    form_class = forms.LessonForm
    template_name = 'courses/lesson-form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user in self.get_object().chapter.course.teachers.all()

    def get_success_url(self):
        return reverse('courses:lessons', kwargs={'pk': self.object.chapter.course.pk})+f'?lesson_id={self.object.id}'

class UpdateHomeworkView(UserPassesTestMixin, UpdateView):
    model = models.Homework
    form_class = forms.HomeWorkForm
    template_name = 'courses/homework-form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user in self.get_object().lesson.chapter.course.teachers.all()

    def get_success_url(self):
        return reverse('courses:lessons', kwargs={'pk': self.object.lesson.chapter.course.pk})+f'?lesson_id={self.object.lesson.id}'

class CoursesListView(ListView):
    model = models.Course
    template_name = 'courses/courses-list.html'
    context_object_name = 'courses'
    queryset = models.Course.shown_objects.all()
    paginate_by = 5
    ordering = ['-created']

class CourseDetailView(DetailView):
    model = models.Course
    template_name = 'courses/course-detail.html'
    context_object_name = 'course'

class CourseLessonsView(UserPassesTestMixin, DetailView):
    model = models.Course
    template_name = 'courses/course-lessons.html'
    context_object_name = 'course'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user in self.get_object().teachers.all() or self.request.user in self.get_object().students.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('lesson_id', False):
            context['active_lesson'] = models.Lesson.objects.filter(id=self.request.GET['lesson_id']).first()
        else:
            context['active_lesson'] = context['course'].course_chapters.first().chapter_lessons.first()
        context['hw_respond_form'] = forms.HomeWorkRespondForm()
        context['chapter_form'] = forms.CourseChapterForm()
        context['lesson_form'] = forms.LessonForm()
        context['commentary_form'] = forms.HWRespondCommentaryForm()
        return context

class HomeWorkRespondView(View):
    def post(self, request, course_id, lesson_id):
        course = get_object_or_404(models.Course, id=course_id)
        active_lesson = get_object_or_404(models.Lesson, id=lesson_id)
        lesson_homework = models.Homework.objects.filter(lesson=active_lesson).first()
        form = forms.HomeWorkRespondForm(request.POST, request.FILES)
        if form.is_valid():
            new_homework_respond = models.HomeWorkRespond(
                homework = lesson_homework,
                student = request.user,
                text = form.cleaned_data['text'],
                file_attachment = form.cleaned_data['file_attachment']
            )
            new_homework_respond.save()

        return HttpResponseRedirect(reverse('courses:lessons', kwargs = {'pk': course.pk})+f'?lesson_id={lesson_id}')

class HWRespondCommentView(LoginRequiredMixin, View):
    def post(self, request, hw_respond_id):
        homework_respond = get_object_or_404(models.HomeWorkRespond, id=hw_respond_id)
        commentary_form = forms.HWRespondCommentaryForm(request.POST)
        if commentary_form.is_valid() and commentary_form.has_changed():
            new_commentary = models.HWRespondCommentary(
                author=request.user,
                text=commentary_form.cleaned_data['text'],
                homework_respond=homework_respond
            )
            new_commentary.save()

            active_lesson = homework_respond.homework.lesson
            active_course = active_lesson.chapter.course

            return HttpResponseRedirect(reverse('courses:lessons', kwargs = {'pk': active_course.pk})+f'?lesson_id={active_lesson.id}')

class AcceptHWRespondView(LoginRequiredMixin, View):
    def post(self, request, hw_respond_id):
        homework_respond = get_object_or_404(models.HomeWorkRespond, id=hw_respond_id)
        homework_respond.is_accepted = True
        homework_respond.save()
        active_lesson = homework_respond.homework.lesson
        active_course = active_lesson.chapter.course

        return HttpResponseRedirect(reverse('courses:lessons', kwargs = {'pk': active_course.pk})+f'?lesson_id={active_lesson.id}')
