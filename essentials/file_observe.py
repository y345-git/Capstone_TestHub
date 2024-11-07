import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if the event is a file modification (not a directory)
        if not event.is_directory:
            print(f"File modified: {event.src_path}")

    def on_created(self, event):
        # Detect newly created files
        if not event.is_directory:
            print(f"New file created: {event.src_path}")

    def on_deleted(self, event):
        # Detect deleted files
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")

    def on_moved(self, event):
        # Detect moved files
        if not event.is_directory:
            print(f"File moved: {event.src_path} to {event.dest_path}")

def monitor_folder(folder_path):
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()
    print(f"Monitoring changes in folder: {folder_path}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping folder monitoring.")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python monitor_folder.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    monitor_folder(folder_path)
