from django.urls import path
from . import views

app_name = 'studylogs'

urlpatterns = [
    path('', views.log_list, name='list'),
    path('add/', views.log_add, name='add'),
    path('<int:pk>/edit/', views.log_edit, name='edit'),
    path('<int:pk>/delete/', views.log_delete, name='delete'),
]
