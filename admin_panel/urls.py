from django.urls import path
from . import views


urlpatterns = [

    path('admindash', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('manage-users/', views.manage_users, name='manage_users'),
    path('pending-users/', views.pending_users, name='pending_users'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('decline-user/<int:user_id>/', views.decline_user, name='decline_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('manage-items/', views.manage_items, name='manage_items'),

]