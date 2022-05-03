from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class ShareFileAdmin (admin.ModelAdmin):
    list_display = ('file', 'user')

class ShareDirectoryAdmin (admin.ModelAdmin):
    list_display = ('directory', 'user')

class FileAdmin (admin.ModelAdmin):
    list_display = ('filename', 'owner', 'upload_time', 'parent')
    list_display_links = ('filename',)

    
class DirectoryAdmin (admin.ModelAdmin):
    list_display = ('pk','name', 'owner', 'parent')


class UserAdmin(UserAdmin):

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username','email', 'password1', 'password2', ),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Directory,DirectoryAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(SharedFile, ShareFileAdmin)
admin.site.register(SharedDirectory, ShareDirectoryAdmin)