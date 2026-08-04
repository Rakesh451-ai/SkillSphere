from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.cpp_calculator, name='cpp_calculator'),
    path('cpp-calculator/', views.cpp_calculator),
    path('games/update-progress/', views.update_game_progress, name='update_game_progress'),
    path('study/', views.study_materials, name='study_materials'),
    path('study/toggle-problem/', views.toggle_dsa_problem, name='toggle_dsa_problem'),
    path('dsa-visualizer/', views.dsa_visualizer, name='dsa_visualizer'),
    path('admin-users/', views.admin_user_dashboard, name='admin_user_dashboard'),
    path('admin-users/create/', views.admin_user_create, name='admin_user_create'),
    path('admin-users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin-users/<int:user_id>/toggle/', views.admin_user_toggle_status, name='admin_user_toggle_status'),
    path('admin-users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin-notifications/broadcast/', views.admin_send_broadcast_notification, name='admin_send_broadcast_notification'),
    path('discussions/', views.discussions_list, name='discussions'),
    path('discussions/create/', views.discussion_create, name='discussion_create'),
    path('discussions/<int:post_id>/', views.discussion_detail, name='discussion_detail'),
    path('discussions/<int:post_id>/reply/', views.discussion_reply, name='discussion_reply'),
    path('discussions/<int:post_id>/upvote/', views.discussion_upvote, name='discussion_upvote'),
    path('discussions/<int:post_id>/delete/', views.discussion_delete, name='discussion_delete'),
    path('chat/', views.general_chat, name='general_chat'),
    path('chat/api/messages/', views.chat_api_messages, name='chat_api_messages'),
    path('chat/api/send/', views.chat_api_send, name='chat_api_send'),
    path('chat/<int:message_id>/delete/', views.chat_message_delete, name='chat_message_delete'),

    # Quiz Routes
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/<int:quiz_id>/take/', views.quiz_take, name='quiz_take'),
    path('quizzes/<int:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    path('quizzes/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),

    # Admin Quiz Management Routes
    path('admin-quizzes/', views.admin_quiz_list, name='admin_quiz_list'),
    path('admin-quizzes/create/', views.admin_quiz_create, name='admin_quiz_create'),
    path('admin-quizzes/<int:quiz_id>/edit/', views.admin_quiz_edit, name='admin_quiz_edit'),
    path('admin-quizzes/<int:quiz_id>/add-question/', views.admin_quiz_add_question, name='admin_quiz_add_question'),
    path('admin-quizzes/question/<int:question_id>/delete/', views.admin_quiz_delete_question, name='admin_quiz_delete_question'),
    path('admin-quizzes/<int:quiz_id>/delete/', views.admin_quiz_delete, name='admin_quiz_delete'),
]

