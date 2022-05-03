from django.contrib import admin
from .models import *
# Register your models here.

class ShareFileAdmin (admin.ModelAdmin):
    list_display = ('file', 'user')

class ShareDirectoryAdmin (admin.ModelAdmin):
    list_display = ('directory', 'user')

class FileAdmin (admin.ModelAdmin):
    list_display = ('pk','uploaded_file', 'owner', 'upload_time', 'parent')
    
class DirectoryAdmin (admin.ModelAdmin):
    list_display = ('pk','name', 'owner', 'parent')

admin.site.register(Directory,DirectoryAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(SharedFile, ShareFileAdmin)
admin.site.register(SharedDirectory, ShareDirectoryAdmin)