from django.urls import path
from .views import *

app_name = 'cloud'

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload, name='upload'),
    path('upload-file/', save_file, name='upload-file'),
    
]