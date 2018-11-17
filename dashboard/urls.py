from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('needy_list/', views.needy_list, name='needy_list'),
]
