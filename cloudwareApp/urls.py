from django.urls import path
from .views import *
from django.conf.urls.static import static

app_name = 'cloud'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup/', signup, name='signup'),
    path('validate_signup/', validate_signup, name='validate_signup'),
    path('login/', login_view, name='login'),
    path('login/authenticate', authenticate_view, name='authenticate'),
    path('logout', logout_view, name="logout"),
    path('uploaded_files/<int:fileId>', downloadFile, name='downloadFile'),
    path('upload/', upload, name='upload'),
    path('cloudware-app/', cloudware_app, name='cloudware_app'),
    path('profile/', profile, name='profile'),
    path('share-file/<int:fileId>', shareFile, name="shareFile"),
    path('upload_file', upload_file, name='upload_file'),
    path('delete_file', delete_file, name='delete_file'),
    path('edit_file', edit_file, name='edit_file'),
    path('create_directory', create_directory, name='create_directory'),
    path('directories', directories, name='directory'),
    path('directory/<int:dir_id>', get_directory, name='get_directory'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "cloudwareApp.views.page_not_found"
