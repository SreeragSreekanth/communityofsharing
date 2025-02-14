from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.view_notifications, name='view_notifications'),
]