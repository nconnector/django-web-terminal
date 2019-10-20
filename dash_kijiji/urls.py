

from django.urls import path
from . import views


urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('login/', views.Login.as_view(), name='login'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('about/', views.About.as_view(), name='about'),

    path('flow/', views.Flow.as_view(), name='flow'),
]
