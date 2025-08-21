from django.contrib import admin
from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'status', 'progress', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('filename',)

