from django.urls import path
from .views import *
from django.conf.urls.static import static

app_name = 'cloud'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup', signup, name='signup'),
    path('validate_signup', validate_signup, name='validate_signup'),
    path('login', login_view, name='login'),
    path('login/authenticate', authenticate_view, name='authenticate'),
    path('logout', logout_view, name="logout"),
    path('download_file/<int:fileId>', downloadFile, name='downloadFile'),
    path('upload', upload, name='upload'),
    path('cloudware-app', file_manager, name='cloudware_app'),
    path('cloudware-app/<int:dir_id>', get_directory, name='cloudware_app_get_directory'),
    path('cloudware-app/shared-files',shared_sources, name='shared_files'),
    path('cloudware-app/shared-files/<int:dir_id>',get_share_directory, name='shared_files'),
    path('profile', profile, name='profile'),
    path('share-file/<int:fileId>', shareFile, name="shareFile"),
    path('share-directory/<int:directoryId>', share_directory, name="shareDirectory"),
    path('upload_file', upload_file, name='upload_file'),
    path('delete_file', delete_file, name='delete_file'),
    path('delete_directory', delete_directory, name='delete_directory'),
    path('edit_file', edit_file, name='edit_file'),
    path('edit_directory', edit_directory, name='edit_directory'),
    path('create_directory', create_directory, name='create_directory'),
    path('update_username', update_username, name="update_username"),
    path('update_email', update_email, name="update_email"),
    path('update_password', update_password, name="update_password"),
    path('delete_account', delete_account, name="delete_account"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "cloudwareApp.views.page_not_found"
