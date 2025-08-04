from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('comment/create/', views.comment_create_view, name='comment_create'),
    path('comment/<int:comment_id>/delete/', views.comment_delete_view, name='comment_delete'),
    path('post/create/', views.post_create_view, name='post_create'),
    path('post/<int:post_id>/like/', views.post_like, name='post_like'),
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
]