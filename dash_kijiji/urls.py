

from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('login/', views.Login.as_view(), name='login'),
    path('about/', views.About.as_view(), name='about'),

    path('case/<case_id>/', views.ViewCase.as_view(), name='case'),

]

