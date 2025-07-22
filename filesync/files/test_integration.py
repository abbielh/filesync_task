import os
import tempfile
import time
import shutil

from django.test import LiveServerTestCase
from files.models import SyncedFile  
from sync_app import SyncHandler  


class SyncHandlerE2ETest(LiveServerTestCase):
    def setUp(self):
        # Override the client API_URL and SOURCE_DIR dynamically
        self.old_api_url = SyncHandler.__init__.__globals__['API_URL']
        self.old_source_dir = SyncHandler.__init__.__globals__['SOURCE_DIR']

        self.api_url = f"{self.live_server_url}/api/files/"
        self.temp_dir = tempfile.mkdtemp()

        # Patch the constants used in SyncHandler
        SyncHandler.__init__.__globals__['API_URL'] = self.api_url
        SyncHandler.__init__.__globals__['SOURCE_DIR'] = self.temp_dir

        self.handler = SyncHandler()

    def tearDown(self):
        # Restore original globals
        SyncHandler.__init__.__globals__['API_URL'] = self.old_api_url
        SyncHandler.__init__.__globals__['SOURCE_DIR'] = self.old_source_dir

        shutil.rmtree(self.temp_dir)

    def test_upload_file_end_to_end(self):
        # Create file in temp source dir
        file_name = "example.txt"
        file_path = os.path.join(self.temp_dir, file_name)
        with open(file_path, "w") as f:
            f.write("Hello E2E")

        # Run initial sync
        self.handler.initial_sync()
        time.sleep(0.5)

        # Check it's uploaded
        self.assertIn(file_name, self.handler.synced_files)
        file_id = self.handler.synced_files[file_name]

        # Verify it's in the Django DB
        self.assertTrue(SyncedFile.objects.filter(id=file_id, name=file_name).exists())

    def test_delete_file_end_to_end(self):
        # First upload
        file_name = "todelete.txt"
        file_path = os.path.join(self.temp_dir, file_name)
        with open(file_path, "w") as f:
            f.write("To be deleted")

        self.handler.initial_sync()
        time.sleep(0.5)
        self.assertIn(file_name, self.handler.synced_files)

        # Delete locally
        os.remove(file_path)
        self.handler.initial_sync()
        time.sleep(0.5)

        # Confirm deletion from synced_files and DB
        self.assertNotIn(file_name, self.handler.synced_files)
        self.assertFalse(SyncedFile.objects.filter(name=file_name).exists())
