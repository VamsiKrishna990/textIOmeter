import time
from threading import Event
import shutil

# Define shared_data at the module level so it can be imported by other modules
shared_data = {'word_count': 0}

def autosave(stop_event, main_file_path, staging_file_path, interval=5):
    """Automatically save the file and update word count every specified interval until stopped, using a buffer."""
    while not stop_event.is_set():
        try:
            # Copy the main file to the staging file
            shutil.copy(main_file_path, staging_file_path)

            # Read the contents of the staging file
            with open(staging_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Calculate and update the word count
            words = content.split()
            shared_data['word_count'] = len(words)
            print(f"File copied and word count updated... Word count: {shared_data['word_count']}")

        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(interval)
