from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('analytics/', views.analytics, name='analytics'),
    path('games/', views.cpp_calculator, name='cpp_calculator'),
    path('games/update-progress/', views.update_game_progress, name='update_game_progress'),
    path('study/', views.study_materials, name='study_materials'),
    path('study/toggle-problem/', views.toggle_dsa_problem, name='toggle_dsa_problem'),
]
