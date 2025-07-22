from rest_framework import serializers
from .models import SyncedFile

# Used in the views to process incoming/outgoing data
class SyncedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncedFile
        fields = ['id', 'name', 'file', 'timeUploaded', 'timeUpdated']
