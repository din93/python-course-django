from django.urls import path
from blog import views

urlpatterns = [
    path('', views.BlogHomeView.as_view(), name='home'),
    path('create/', views.CreateArticleView.as_view(), name='create'),
    path('create_comment/<int:article_id>/', views.CreateCommentView.as_view(), name='create_comment'),
    path('update/<int:pk>/', views.UpdateArticleView.as_view(), name='update'),
    path('detail/<int:pk>/', views.DetailArticleView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.DeleteArticleView.as_view(), name='delete'),
]
