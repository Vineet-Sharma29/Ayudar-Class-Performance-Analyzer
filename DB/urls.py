from . import views
from django.urls import path,re_path


urlpatterns=[
    re_path('^$',views.uselesspage,name = 'DB.uselesspage'),
    path('output/',views.output,name = 'DB.result')

]