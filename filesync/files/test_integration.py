import os
import tempfile
import time
import shutil

from django.test import LiveServerTestCase
from files.models import SyncedFile  
from sync_app import SyncHandler  


class SyncHandlerE2ETest(LiveServerTestCase):
    # Creates a temporary directory for testing by overriding the API_URL and the source dir to a temporary folder.
    def setUp(self):
        self.old_api_url = SyncHandler.__init__.__globals__['API_URL']
        self.old_source_dir = SyncHandler.__init__.__globals__['SOURCE_DIR']

        self.api_url = f"{self.live_server_url}/api/files/"
        self.temp_dir = tempfile.mkdtemp()

        SyncHandler.__init__.__globals__['API_URL'] = self.api_url
        SyncHandler.__init__.__globals__['SOURCE_DIR'] = self.temp_dir

        self.handler = SyncHandler()

    # Cleans the temp directory and restores the intended API_URL and source directory
    def tearDown(self):
        SyncHandler.__init__.__globals__['API_URL'] = self.old_api_url
        SyncHandler.__init__.__globals__['SOURCE_DIR'] = self.old_source_dir

        shutil.rmtree(self.temp_dir)

    # Creates a file in the temp dir and uploads it to the server
    # Checks that the file is recorded in the synced files directory
    # and that the file record exists in the django database (SyncedFile model)
    def test_upload_file_end_to_end(self):
        file_name = "example.txt"
        file_path = os.path.join(self.temp_dir, file_name)
        with open(file_path, "w") as f:
            f.write("Hello E2E")

        self.handler.initial_sync()
        time.sleep(0.5)

        self.assertIn(file_name, self.handler.synced_files)
        file_id = self.handler.synced_files[file_name]

        self.assertTrue(SyncedFile.objects.filter(id=file_id, name=file_name).exists())

    # Uploads a file to the server, then deletes it locally.
    # Checks that the file is removed from the synced files directory
    # and that the file record is removed from the django database (SyncedFile model)
    def test_delete_file_end_to_end(self):
        file_name = "todelete.txt"
        file_path = os.path.join(self.temp_dir, file_name)
        with open(file_path, "w") as f:
            f.write("To be deleted")

        self.handler.initial_sync()
        time.sleep(0.5)
        self.assertIn(file_name, self.handler.synced_files)

        os.remove(file_path)
        self.handler.initial_sync()
        time.sleep(0.5)

        self.assertNotIn(file_name, self.handler.synced_files)
        self.assertFalse(SyncedFile.objects.filter(name=file_name).exists())
