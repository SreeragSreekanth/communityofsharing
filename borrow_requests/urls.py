from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_items, name='search_items'),
    path('manage-requests/', views.manage_requests, name='manage_requests'),
    path('update-request/<int:request_id>/', views.update_request_status, name='update_request_status'),
    path('detail/<int:item_id>/borrow/', views.borrow_request, name='borrow_request'),
]