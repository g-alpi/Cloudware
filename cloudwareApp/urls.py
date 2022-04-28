from django.urls import path
from .views import *

app_name = 'cloud'

urlpatterns = [
    path('', index, name='index'),
    path('uploaded_files/<int:fileId>', downloadFile, name='downloadFile'),
    path('upload/', upload, name='upload'),
    path('upload_file/', save_file, name='upload_file'),
    path('delete_file', delete_file, name='delete_file'),
    path('edit_file', edit_file, name='edit_file'),
]

handler404 = "cloudwareApp.views.page_not_found"
