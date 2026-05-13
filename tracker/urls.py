from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('add-habit/', views.add_habit, name='add_habit'),

    path('complete/<int:habit_id>/', views.complete_habit, name='complete_habit'),

    path('analytics/', views.analytics, name='analytics'),

    path('streaks/', views.streaks, name='streaks'),

    path('add-water/', views.add_water, name='add_water'),

    path('add-steps/', views.add_steps, name='add_steps'),

    path('settings/', views.settings_page, name='settings'),

    
    # AUTH

    path('login/', views.login_page, name='login'),

    path('register/', views.register_page, name='register'),

    path('logout/', views.logout_page, name='logout'),

    path('ai-chat/', views.ai_chat, name='ai_chat'),
]