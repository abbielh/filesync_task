from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import SyncedFile
from django.core.files.uploadedfile import SimpleUploadedFile
import os

# Create your tests here.

class SyncedFileAPITest(APITestCase):
    def setUp(self):
        self.upload_url = reverse('file-list')  # Adjust name if different

    def test_upload_file(self):
        file_content = b"Hello test"
        uploaded_file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")
        data = {'name': 'test.txt', 'file': uploaded_file}

        response = self.client.post(self.upload_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SyncedFile.objects.count(), 1)

        synced_file = SyncedFile.objects.first()
        self.assertEqual(synced_file.name, 'test.txt')
        # Optional: check file exists on disk
        self.assertTrue(os.path.exists(synced_file.file.path))

    def test_list_files(self):
        SyncedFile.objects.create(name="f1.txt", file=SimpleUploadedFile("f1.txt", b"data"))
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_file(self):
        synced_file = SyncedFile.objects.create(name="f1.txt", file=SimpleUploadedFile("f1.txt", b"data"))
        url = reverse('file-detail', args=[synced_file.id])

        new_file = SimpleUploadedFile("f1.txt", b"updated data")
        response = self.client.put(url, {'name': 'f1.txt', 'file': new_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_file(self):
        synced_file = SyncedFile.objects.create(name="f1.txt", file=SimpleUploadedFile("f1.txt", b"data"))
        url = reverse('file-detail', args=[synced_file.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SyncedFile.objects.count(), 0)
