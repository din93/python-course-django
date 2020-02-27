from django.shortcuts import render, get_list_or_404, get_object_or_404
from courses.models import Course, CourseChapter, Lesson, QuizQuestion, QuizOption, Homework, HomeWorkRespond
from courses.forms import HomeWorkRespondForm

def courses_list(request):
    courses = get_list_or_404(Course)
    return render(request, 'courses/courses-list.html', context={'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course-detail.html', context={'course': course})

def course_lessons(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    chapters = CourseChapter.objects.filter(course=course)
    lessons_tree = []
    for chapter in chapters:
        lessons_tree.append(Lesson.objects.filter(chapter=chapter))
    
    active_lesson = get_object_or_404(Lesson, id=request.GET.get('lesson_id', lessons_tree[0][0].id))
    quiz_questions = QuizQuestion.objects.filter(lesson=active_lesson)
    quiz_options_tree = []
    for quiz_question in quiz_questions:
        quiz_options_tree.append(QuizOption.objects.filter(question=quiz_question))

    lesson_homework = Homework.objects.filter(lesson=active_lesson).first()
    if request.method=='POST':
        form = HomeWorkRespondForm(request.POST, request.FILES)
        if form.is_valid():
            new_homework_respond = HomeWorkRespond(
                homework = lesson_homework,
                student = None,
                text = form.cleaned_data['text'],
                file_attachment = form.cleaned_data['file_attachment']
            )
            new_homework_respond.save()
    else:
        form = HomeWorkRespondForm()
    homework_respond = HomeWorkRespond.objects.filter(homework=lesson_homework).first()

    return render(
        request,
        'courses/course-lessons.html',
        context={
            'course': course,
            'chapters': chapters,
            'lessons_tree': lessons_tree,
            'active_lesson': active_lesson,
            'quiz_questions': quiz_questions,
            'quiz_options_tree': quiz_options_tree,
            'lesson_homework': lesson_homework,
            'homework_respond': homework_respond,
            'form': form
        }
    )
