from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('download_video/<path:video_src>/', views.download_video, name='download_video'),
]