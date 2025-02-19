from django.urls import path
from . import views

urlpatterns = [
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('events/', views.events_list, name='events_list'),
    path('postcreate/', views.create_announcement, name='create_announcement'),
    path('postedit/<int:pk>/', views.edit_announcement, name='edit_announcement'),
    path('delete_announcement/<int:pk>/', views.delete_announcement, name='delete_announcement'),

    path('eventcreate/', views.create_event, name='create_event'),
    path('eventedit/<int:pk>/', views.edit_event, name='edit_event'),
    path('delete_event/<int:pk>/', views.delete_event, name='delete_event'),
]
