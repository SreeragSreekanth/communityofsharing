from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_item, name='create_item'),
    path('edit/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('list/', views.item_list, name='item_list'),
    path('detail/<int:item_id>/', views.item_detail, name='item_detail'),
]