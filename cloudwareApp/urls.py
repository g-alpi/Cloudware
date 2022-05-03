from msilib import _directories
from django.urls import path
from .views import *
from django.conf.urls.static import static

app_name = 'cloud'

urlpatterns = [
    path('', index, name='index'),
    path('uploaded_files/<int:fileId>', downloadFile, name='downloadFile'),
    path('upload/', upload, name='upload'),
    path('upload_file', upload_file, name='upload_file'),
    path('delete_file', delete_file, name='delete_file'),
    path('edit_file', edit_file, name='edit_file'),
    path('create_directory', create_directory, name='create_directory'),
    path('directories', directories, name='directory'),
    path('directory/<int:dir_id>', get_directory, name='get_directory'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "cloudwareApp.views.page_not_found"
