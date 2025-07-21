from django.contrib import admin
from .models import SyncedFile
# Register your models here.

@admin.register(SyncedFile)
class SyncedFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'timeUploaded', 'timeUpdated')
    search_fields = ('name',)
