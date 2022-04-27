from django.db import models
from django.contrib.auth.models import User


class Directory (models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Directories"

    def __str__(self):
        return self.name

class File (models.Model):
    uploaded_file = models.FileField(upload_to = "uploaded_files/")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    father = models.ForeignKey(Directory, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.uploaded_file)
    
class SharedFile(models.Model):
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_id.name + ' -> ' + self.user_id.username

class SharedDirectory (models.Model):
    directoy_id = models.ForeignKey(Directory, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Shared Directories"

    def __str__(self):
        return self.directoy_id.name + ' -> ' + self.user_id.username