from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<str:filename>/', views.stream_video, name='stream_video'),
    path('videos/<str:video_name>/', views.get_video, name='get_video'),
    path('live/', views.go_live, name='go_live'),
]
