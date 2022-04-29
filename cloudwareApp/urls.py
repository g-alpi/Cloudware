from django.urls import path
from .views import *

app_name = 'cloud'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('uploaded_files/<int:fileId>', downloadFile, name='downloadFile'),
    path('upload/', upload, name='upload'),
    path('upload-file/', save_file, name='upload-file'),
    path('share-file/<int:fileId>', shareFile, name="shareFile"),
]

handler404 = "cloudwareApp.views.page_not_found"
