from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_items, name='search_items'),
    path('request/<int:item_id>/', views.send_borrow_request, name='send_borrow_request'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('update-request/<int:request_id>/', views.update_request_status, name='update_request_status'),
]