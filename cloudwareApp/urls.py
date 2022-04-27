from django.urls import path
from .views import *

app_name = 'cloud'

urlpatterns = [
    path('', index, name='index'),
    path('uploaded_files/<int:fileId>', downloadFile, name='downloadFile'),
    path('upload/', upload, name='upload'),
    path('upload-file/', save_file, name='upload-file'),
]

handler404 = "cloudwareApp.views.page_not_found"
