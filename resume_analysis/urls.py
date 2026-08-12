from django.urls import path
from . import views

app_name = 'resume_analysis'

urlpatterns = [
    path('', views.resume_upload, name='upload'),
    path('result/<int:pk>/', views.resume_result, name='result'),
]
