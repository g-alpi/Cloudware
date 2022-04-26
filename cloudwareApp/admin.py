from django.contrib import admin
from .models import Directory, File, ShareFile, ShareDirectory
# Register your models here.

class ShareFileAdmin (admin.ModelAdmin):
    list_display = ('file_id', 'user_id')

class ShareDirectoryAdmin (admin.ModelAdmin):
    list_display = ('directoy_id', 'user_id')

admin.site.register(Directory)
admin.site.register(File)
admin.site.register(ShareFile, ShareFileAdmin)
admin.site.register(ShareDirectory, ShareDirectoryAdmin)

