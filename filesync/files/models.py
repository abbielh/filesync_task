from django.db import models

# Create your models here.
# Stores the file ID, file name and contents and time uploaded/updated. 
# When a change is detected, updates occur automatically.

class SyncedFile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    file = models.FileField(upload_to='files/')
    timeUploaded = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name