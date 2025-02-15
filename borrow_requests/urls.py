from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_items, name='search_items'),
    path('request/<int:item_id>/', views.request_borrow, name='request_borrow'),
    path('manage/', views.manage_requests, name='manage_requests'),
    path('manage/approve/<int:request_id>/', views.approve_request, name='approve_request'),
    path('manage/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('manage/return/<int:request_id>/', views.mark_as_returned, name='mark_as_returned'),
    path('borrowed-items/', views.borrowed_items, name='borrowed_items'),
    path('lended-items/', views.lended_items, name='lended_items'),

]