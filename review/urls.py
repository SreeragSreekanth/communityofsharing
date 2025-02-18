from django.urls import path
from . import views

urlpatterns = [
    path('leave/<int:user_id>/', views.leave_review, name='leave_review'),
    path('edit-review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
]
