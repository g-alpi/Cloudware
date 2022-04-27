from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('uploaded_files/<int:fileId>', downloadFile, name='downloadFile'),
]

handler404 = "cloudwareApp.views.page_not_found"