from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('change-password/', views.change_password, name='change_password'),
]