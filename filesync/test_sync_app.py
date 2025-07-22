import tempfile
import os
from unittest.mock import patch, MagicMock
from sync_app import SyncHandler

# Mock tests to ensure that files are being created and deleted
# Essentially checks the synced_files dictionary for files and their ID's and whether they have been modified correctly.
def test_upload_new_file():
    handler = SyncHandler()
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file_path = os.path.join(tmpdir, "newfile.txt")
        with open(test_file_path, "w") as f:
            f.write("hello")

        # Patch requests.post to simulate API response
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 201
            mock_post.return_value.json.return_value = {"id": 123}

            handler.upload_file("newfile.txt", test_file_path)

            assert handler.synced_files["newfile.txt"] == 123
            mock_post.assert_called_once()

def test_delete_file():
    handler = SyncHandler()
    handler.synced_files = {"oldfile.txt": 456}

    with patch("requests.delete") as mock_delete:
        mock_delete.return_value.status_code = 204

        handler.delete_file("oldfile.txt")

        assert "oldfile.txt" not in handler.synced_files
        mock_delete.assert_called_once()
