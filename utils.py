"""
This script provides utility functions and configurations for a PyQt-based GUI application. 
Modules:
    - os: Provides functions for interacting with the operating system.
    - platform: Provides a way to access underlying platform’s data.
    - shutil: Provides functions to operate on files and collections of files.
    - csv: Provides functionality to read and write CSV files.
    - json: Provides methods for parsing and creating JSON data.
    - PyQt5.QtWidgets.QDesktopWidget: Provides screen-related information and utilities.
    - PyQt5.QtWidgets.QMessageBox: Provides a dialog box to display messages to the user.
"""

import json
import os
import platform
import shutil
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QMessageBox
import pandas as pd
from PyQt5.QtGui import QTextCursor


def create_directory(folder_path):
    """
    Ensure that the specified log folder exists. If it doesn't exist, create it.

    Args:
        folder_path (str): The path to the log folder.

    Returns:
        None
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"Created log folder: {folder_path}")
    else:
        print(f"Log folder already exists: {folder_path}")


def show_message_box(parent, icon_type, title, text):
    """
    Display a message box with specified icon, title, and text.

    Args:
        parent (QWidget or None): Parent widget of the message box.
        icon_type (QMessageBox.Icon): Icon type to display (e.g., QMessageBox.Information, QMessageBox.Question).
        title (str): Title of the message box.
        text (str): Text content of the message box.

    Returns:
        StandardButton: Button clicked by the user (QMessageBox.Yes or QMessageBox.No for question icon, QMessageBox.Ok for other icons).
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(icon_type)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    (
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if icon_type == QMessageBox.Question
        else msg_box.setStandardButtons(QMessageBox.Ok)
    )
    return msg_box.exec_()


def center_window(window):
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())


def find_chrome_path():
    system = platform.system()
    print(f"System: {system}")
    if system == "Windows":
        possible_paths = [
            os.path.join(
                os.environ.get("ProgramFiles", "C:\\Program Files"),
                "Google",
                "Chrome",
                "Application",
                "chrome.exe",
            ),
            os.path.join(
                os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
                "Google",
                "Chrome",
                "Application",
                "chrome.exe",
            ),
        ]
        windows_specific_paths = [
            os.path.join(
                os.environ.get("LOCALAPPDATA", "C:\\Users\\%USERNAME%\\AppData\\Local"),
                "Google\\Chrome\\Application\\chrome.exe",
            ),
            os.path.join(
                os.environ.get("APPDATA", "C:\\Users\\%USERNAME%\\AppData\\Roaming"),
                "Google\\Chrome\\Application\\chrome.exe",
            ),
        ]
        possible_paths.extend(windows_specific_paths)
        chrome_path = next(
            (path for path in possible_paths if os.path.exists(path)), None
        )
        temp_dir = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "chrome_temp")
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except OSError as e:
            print(f"Error: {e.strerror}")

        return chrome_path
    elif system == "Linux":
        chrome_path = shutil.which("google-chrome") or shutil.which(
            "google-chrome-stable"
        )
        if chrome_path:
            return chrome_path
        linux_specific_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/opt/google/chrome/google-chrome",
        ]
        return next(
            (path for path in linux_specific_paths if os.path.exists(path)), None
        )
    return None


async def page_load(page, pageurl):
    # Navigate to the page and wait for DOM content to be loaded
    response = await page.goto(pageurl, waitUntil="domcontentloaded")
    print(response)
    # Check response status using ternary operators
    return False if response.status in [404, 403] else True


def print_the_output_statement(output, message):
    output.append(f"<b>{message}</b> \n \n")
    # Print the message to the console
    output.moveCursor(QTextCursor.End)
    print(message)


def convert_into_csv_and_save(json_data, out_put_csv):
    report_directory = os.path.dirname(out_put_csv)
    # print("report_directory", report_directory)

    create_directory(report_directory)
    df = pd.DataFrame(json_data)
    df.to_csv(
        out_put_csv, index=False
    )  # Set index=False to exclude DataFrame index in the CSV output
    print(f"json to csv converted successfully with the {out_put_csv} ")


def load_stylesheet(file_path):
    with open(file_path, "r") as file:
        stylesheet = file.read()
    return stylesheet


# Additional code and function definitions go here


def xlsx_to_json(xlsx_file_path):
    df = pd.read_excel(xlsx_file_path)
    data_dict = df.to_dict(orient="records")
    json_data = json.dumps(data_dict, indent=4)
    num_records = len(df)
    header_columns = list(df.columns)
    return header_columns, json_data, num_records


def parse_json(json_string):
    """
    Parses a JSON string and returns a Python dictionary.

    Args:
        json_string (str): The JSON string to be parsed.

    Returns:
        dict: The parsed JSON data as a Python dictionary.

    Raises:
        JSONDecodeError: If the JSON string cannot be decoded.
        Exception: If any other error occurs during parsing.
    """
    try:
        json_data = json.loads(json_string)
        return json_data
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e)
    except Exception as e:
        print("An error occurred:", e)


def is_valid_json(json_string):
    """
    Checks if a given string is a valid JSON.
    Args:
        json_string (str): The JSON string to be validated.
    Returns:
        bool: True if the JSON string is valid, False otherwise.
    """
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False


def reformat_data(data):
    # Create a list to store reformatted dictionaries
    reformatted_data = []
    # Iterate through each dictionary in the input list
    for entry in data:
        # Create a new dictionary to hold the reformatted key-value pairs
        new_entry = {}
        # Ensure all expected keys are present, with default empty strings or values
        keys = ['expirationDate', 'lastName', 'reportDate', 'service', 'status', 'training', 'record status']
        for key in keys:
            new_entry[key] = entry.get(key, '')
        # Append the reformatted dictionary to the list
        reformatted_data.append(new_entry)
    return reformatted_data
