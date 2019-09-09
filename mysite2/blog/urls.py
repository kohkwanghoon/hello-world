from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name="post_new"),
    path('post/<int:pk>/edit/', views.post_edit, name="post_edit"),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    # 1버전대 문법
    # url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    # 위의 문법에서 url -> path로 대체되었음
    # r'^ 으로 시작하던 부분은 '로 대체되었음
    # (?P<pk>\d+) 는 <int:pk>로 대체되었음
    # 패턴 마지막에 $를 붙이지 않아도 됨
    ]