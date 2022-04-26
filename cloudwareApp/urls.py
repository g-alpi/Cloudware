from django.urls import path
from .views import *

app_name = 'cloud'

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload, name='upload'),
    
]