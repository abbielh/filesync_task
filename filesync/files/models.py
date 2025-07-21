from django.db import models

# Create your models here.

class SyncedFile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    file = models.FileField(upload_to='files/')
    timeUploaded = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name