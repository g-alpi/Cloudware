from urllib import request
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import os

class User (AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=254, unique=True)

class Directory (models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Directories"

    def __str__(self):
        return self.name


def file_path(file, filename):
    if file.parent != None:
        path = get_full_path(file.parent)
        return os.path.join(settings.MEDIA_ROOT, 'uploaded_files',file.owner.username, *path[::-1], filename)
    
    else:
        return os.path.join(settings.MEDIA_ROOT, 'uploaded_files',file.owner.username, filename)

def get_full_path(directory):
    path = []
    actual_directory = directory

    while actual_directory != None:
        path.append(actual_directory.name)
        actual_directory = actual_directory.parent
    return path

class File (models.Model):
    uploaded_file = models.FileField(upload_to=file_path, max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(Directory, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.uploaded_file)
    def filename(self):
        return os.path.basename(self.uploaded_file.name)
    def extension(self):
        return os.path.splitext(self.uploaded_file.name)[1]

    
class SharedFile(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'file',)

    def __str__(self):
        return str(self.file.uploaded_file) + ' -> ' + self.user.username

class SharedDirectory (models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Shared Directories"

    def __str__(self):
        return self.directoy.name + ' -> ' + self.user.username