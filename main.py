import os.path
import sys
import time
import logging
import shutil
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):

        #If the event created is a file then the following code is executed
        if not event.is_directory:
            destination_folder = "C:/Users/Alphy/Desktop/Repository/"

            #If the destination folder does not exist, then it creates the folder
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            
            #Extracts the extension from the path
            path = event.src_path.split("\\")
            extension = path[-1].split(".")[-1]
            file_name = path[-1].split(".")[-2]

            now = datetime.now()
            current_date = now.date()

            #Appends the current date to the destination folder
            destination_path = destination_folder+str(current_date)

            #If the destination folder with the currrent date does not exist, then it creates the folder
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            
            #If the destination folder with the currrent date and extension does not exist, then it creates the folder
            extension_path = destination_path + "/" + extension
            if not os.path.exists(extension_path):
                os.makedirs(extension_path)

            #Calculates the file name
            counter = 1
            file = extension_path + "/" + path[-1]

            #If the file name already exists then it appends a version number to the file name
            while True:
                if os.path.exists(file):
                    file = extension_path + "/" + str(counter) + "-" + path[-1] 
                    counter += 1
                else:
                    break
            
            try:
                #Moves the file to the correct folder
                shutil.move(event.src_path, file)
            except:
                print("Permission denied: Unable to move file")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename="E:\Technologies\Desktop Cleaner - Logging/monitor.log", filemode="a")
    path = "C:/Users/Alphy/Desktop"

    log_event_handler = LoggingEventHandler()
    file_event_handler = NewFileHandler()

    log_observer = Observer()
    log_observer.schedule(log_event_handler, path, recursive=True)
    log_observer.start()

    file_observer = Observer()
    file_observer.schedule(file_event_handler, path, recursive=False)
    file_observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log_observer.stop()
        file_observer.stop()

    log_observer.join()
    file_observer.join()