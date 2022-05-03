from django.urls import path
from .views import *

app_name = 'cloud'

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('login/authenticate', authenticate_view, name='authenticate'),
    path('logout', logout_view, name="logout"),
    path('uploaded_files/<int:fileId>', downloadFile, name='downloadFile'),
    path('upload/', upload, name='upload'),
    path('upload-file/', save_file, name='upload-file'),
    path('cloudware-app/', cloudware_app, name='cloudware_app'),
    path('profile/', profile, name='profile'),
    path('share-file/<int:fileId>', shareFile, name="shareFile"),
]

handler404 = "cloudwareApp.views.page_not_found"
