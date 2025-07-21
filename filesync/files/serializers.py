from rest_framework import serializers
from .models import SyncedFile

class SyncedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncedFile
        fields = ['id', 'name', 'file', 'timeUploaded', 'timeUpdated']
