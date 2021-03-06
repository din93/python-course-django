from django.urls import path
from courses import views

urlpatterns = [
    path('create_course/', views.CreateCourseView.as_view(), name='create_course'),
    path('update_course/<int:pk>/', views.UpdateCourseView.as_view(), name='update_course'),
    path('create_chapter/<int:course_id>/', views.CreateChapterView.as_view(), name='create_chapter'),
    path('update_chapter/<int:pk>/', views.UpdateChapterView.as_view(), name='update_chapter'),
    path('delete_chapter/<int:pk>/', views.DeleteChapterView.as_view(), name='delete_chapter'),
    path('create_lesson/<int:chapter_id>/', views.CreateLessonView.as_view(), name='create_lesson'),
    path('update_lesson/<int:pk>/', views.UpdateLessonView.as_view(), name='update_lesson'),
    path('delete_lesson/<int:pk>/', views.DeleteLessonView.as_view(), name='delete_lesson'),
    path('update_homework/<int:pk>/', views.UpdateHomeworkView.as_view(), name='update_homework'),
    path('list/', views.CoursesListView.as_view(), name='list'),
    path('lessons/<int:pk>/', views.CourseLessonsView.as_view(), name='lessons'),
    path('detail/<int:pk>/', views.CourseDetailView.as_view(), name='detail'),
    path('request_participation/<int:course_id>', views.RequestCourseParticipationView.as_view(), name='request_participation'),
    path('add_teacher/<int:course_id>/<int:user_id>', views.AddTeacherView.as_view(), name='add_teacher'),
    path('add_student/<int:course_id>/<int:user_id>', views.AddStudentView.as_view(), name='add_student'),
    path('hw_respond/<int:course_id>/<int:lesson_id>', views.HomeWorkRespondView.as_view(), name='hw_respond'),
    path('hw_respond_commentary/<int:hw_respond_id>', views.HWRespondCommentView.as_view(), name='hw_respond_commentary'),
    path('accept_hw_respond/<int:hw_respond_id>', views.AcceptHWRespondView.as_view(), name='accept_hw_respond'),
]
