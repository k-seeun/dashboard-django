from django.urls import path

from . import views

app_name = 'pybo'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]