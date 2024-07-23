import asyncio
from datetime import datetime
import os
from screeninfo import get_monitors
import time
from threading import Event

from utils import create_directory

# Configuration settings for the ABC Business Online Portal application.

# Application Settings
APP_TITLE = "ABC Business Online Portal"
APP_NAME = "ABC Business Online Portal"
APP_BUTTON_NAME = "Login"
FILE_TYPE = "csv"
CURRENT_DATE = datetime.now()
FILE_NAME = "ABCGovtWebscrapping"
LOG_TYPE = "log"
LOG_FOLDER = "log"
LOGINURL = "https://abcbiz.abc.ca.gov/login"
HEADLESS = True
monitor = get_monitors()[0]
WIDTH = monitor.width
HEIGHT = monitor.height
THREAD_EVENT = Event()
NEW_EVENT_LOOP = asyncio.new_event_loop()
START_TIME = time.time()


# create_directory(LOG_FOLDER)


# Function to write log entries directly to a file
# def log_entry(log_type, service_id, name, status):
#     # Define the log file name within the log folder
#     log_filename = os.path.join(
#         LOG_FOLDER, f"logfile_{CURRENT_DATE.strftime('%Y-%m-%d_%H-%M-%S')}.{LOG_TYPE}"
#     )
#     # Check if the file already exists to write the header only once
#     file_exists = os.path.isfile(log_filename)
#
#     # Create the log entry
#     log_entry = f"{CURRENT_DATE.strftime('%Y-%m-%d %H:%M:%S')}, {log_type}, {service_id}, {name}, {status}\n"
#
#     # Write the log entry to the file
#     with open(log_filename, "a") as log_file:
#         if not file_exists:
#             # Write the header if the file does not exist
#             log_file.write("Reported Date, ServiceID, Name, Status\n")
#         log_file.write(log_entry)
