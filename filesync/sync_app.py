import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

API_URL = "http://127.0.0.1:8000/api/files/"
SOURCE_DIR = "../data/files"  

class SyncHandler(FileSystemEventHandler):
    def __init__(self):
        self.synced_files = {}  

    # Syncs changes to files when the app starts- e.g if they have been created/deleted locally,
    # yet the changes have not been registered on the server yet.
    def initial_sync(self):
        local_files = set(os.listdir(SOURCE_DIR))
        synced_files = set(self.synced_files.keys())

        for f in local_files - synced_files:
            path = os.path.join(SOURCE_DIR, f)
            if os.path.isfile(path):
                print(f"Initial sync upload: {f}")
                self.upload_file(f, path)

        for f in synced_files - local_files:
            print(f"Initial sync delete remote: {f}")
            self.delete_file(f)

    # Triggered when a file is created, modified, or deleted locally
    def on_created(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        print(f"File created: {filename}")
        self.upload_file(filename, event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        print(f"File modified: {filename}")
        self.upload_file(filename, event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        print(f"File deleted: {filename}")
        self.delete_file(filename)

    # If the file is new: send POST request to create it (calls create view), and stores its ID in the synced files database.
    # If the file is not new: sends PUT request to update existing file on the server using its ID.
    def upload_file(self, name, path):
        if not os.path.exists(path):
            return
        files = {'file': open(path, 'rb')}
        data = {'name': name}

        file_id = self.synced_files.get(name)

        try:
            if file_id:
                url = f"{API_URL}{file_id}/"
                r = requests.put(url, files=files, data=data)
                if r.status_code == 200:
                    print(f"Updated {name}")
            else:
                r = requests.post(API_URL, files=files, data=data)
                if r.status_code == 201:
                    file_id = r.json()['id']
                    self.synced_files[name] = file_id
                    print(f"Uploaded {name}")
        except Exception as e:
            print(f"Failed to sync {name}: {e}")

    # Deletes a certain file using the file's ID, removes it from synced files database
    def delete_file(self, name):
        file_id = self.synced_files.get(name)
        if not file_id:
            print(f"File {name} not found in sync map.")
            return
        try:
            r = requests.delete(f"{API_URL}{file_id}/")
            if r.status_code == 204:
                print(f"Deleted {name} remotely")
                del self.synced_files[name]
        except Exception as e:
            print(f"Failed to delete {name}: {e}")

# Gets the list of already synced files to prevent reuploading existing files as new
def preload_synced_files(handler):
    try:
        r = requests.get(API_URL)
        if r.status_code == 200:
            for f in r.json():
                handler.synced_files[f['name']] = f['id']
            print(f"Preloaded {len(handler.synced_files)} synced files")
    except Exception as e:
        print(f"Could not preload files: {e}")

# Server state is retrieved (all files stored listed) and initial sync ran
# Watch the source directory indefinitely for any changes that should be sent to the server.
def main():
    event_handler = SyncHandler()
    preload_synced_files(event_handler)
    event_handler.initial_sync()

    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()

    print(f"Watching {SOURCE_DIR} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
