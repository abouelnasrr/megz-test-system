from django.urls import path
from . import views

urlpatterns = [
    path('', views.operations_dashboard, name='operations_dashboard'),
    path('post_chat_message/', views.post_chat_message, name='post_chat_message'),
    path('post_announcement/', views.post_announcement, name='post_announcement'),

]
