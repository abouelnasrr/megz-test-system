from django.urls import path
from . import views
# from .views import get_plaintext_password, delete_admin_user, add_admin_user

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # ✅ Add this line
    path('users_dashboard/', views.users_dashboard, name='users_dashboard'),
    path('upload-logo/', views.upload_logo, name='upload_logo'),
    path('remove-logo/', views.remove_logo, name='remove_logo'),
    path("add_admin_user/", views.add_admin_user, name="add_admin_user"),
    path('get_password/<int:user_id>/', views.get_plaintext_password, name='get_password'),
    path('delete_admin_user/<int:user_id>/', views.delete_admin_user, name='delete_admin_user'),
]
