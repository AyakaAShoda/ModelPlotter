from django.urls import path

from . import views

app_name = 'ModelPlotter'
urlpatterns = [
    path('', views.index, name='index'),
    path('test/',views.index2, name='index2'),
    path('plot_model/',views.plot_model,name='plot_model'),
    path('plot_data/',views.plot_data,name='plot_data'),
    path('plot_clear/',views.plot_clear,name='plot_clear'),
    path('manual/',views.manual,name='manual'),
]