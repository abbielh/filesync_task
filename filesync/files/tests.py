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
        self.upload_url = reverse('file-list')

    # Tests file upload
    # Checks that a file is added to the database, the name is correct, and that a 201 response is returned
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

    # Creates one file record in the DB and sends a GET request.
    # Checks that exactly one file is returned in the response JSON, and for a 200 status code.
    def test_list_files(self):
        SyncedFile.objects.create(name="f1.txt", file=SimpleUploadedFile("f1.txt", b"data"))
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # Uploads a file to DB, sends a PUT request to the same file's endpoint.
    # Checks that the status code is 200.
    def test_update_file(self):
        synced_file = SyncedFile.objects.create(name="f1.txt", file=SimpleUploadedFile("f1.txt", b"data"))
        url = reverse('file-detail', args=[synced_file.id])

        new_file = SimpleUploadedFile("f1.txt", b"updated data")
        response = self.client.put(url, {'name': 'f1.txt', 'file': new_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Uploads file to DB, sends a delete request to the same file's endpoint.
    # Checks that there is a 204 status code, and that the DB is now empty.
    def test_delete_file(self):
        synced_file = SyncedFile.objects.create(name="f1.txt", file=SimpleUploadedFile("f1.txt", b"data"))
        url = reverse('file-detail', args=[synced_file.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SyncedFile.objects.count(), 0)
