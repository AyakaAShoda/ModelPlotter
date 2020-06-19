
from django.urls import path

from . import views

app_name = 'ShowLatestPlots'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:optic_name>/', views.plot, name='plot'),
]