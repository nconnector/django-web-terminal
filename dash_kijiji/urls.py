

from django.urls import path
from . import views


urlpatterns = [
    path('', views.test, name='index'),
    path('flow/', views.flow, name='flow')
]