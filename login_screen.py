import sys
import os
import asyncio
from threading import Thread
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from config import *
from scrapping import abiotic_login, scrapping_data
from utils import *
from webdriver import pyppeteerBrowserInit

bootstrap_style = """
QWidget {
    font-family: Arial, sans-serif;
    font-size: 14px;
}
QMainWindow {
    background-color: #f8f9fa;
}
QLabel {
    color: #212529;
}
QLineEdit {
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 5px;
    font-size: 14px;
    color: #495057;
}
QLineEdit:focus {
    border-color: #80bdff;
    outline: 0;
    background-color: rgba(0, 123, 255, 0.1); /* Simulating box-shadow effect */
}
QPushButton {
    background-color: #007bff;
    border: 1px solid #007bff;
    border-radius: 4px;
    color: white;
    padding: 5px 10px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #0056b3;
    border-color: #0056b3;
}
QPushButton:disabled {
    background-color: #6c757d;
    border-color: #6c757d;
    color: white;
}
QTextEdit {
    border: 1px solid #ced4da;
    border-radius: 4px;
    padding: 5px;
    font-size: 14px;
    color: #495057;
    background-color: white;
}
"""

class Worker(QObject):
    login_finished = pyqtSignal(bool, str)
    scrapping_finished = pyqtSignal(bool, list)

    def __init__(self):
        super().__init__()

    def run_login_thread(
        self,
        loop,
        browser,
        username,
        password,
        output_text,
        scrape_thread_event,
    ):
        asyncio.set_event_loop(loop)
        global page
        status, LoginStatus, browser, page = loop.run_until_complete(
            abiotic_login(browser, username, password, output_text)
        )
        self.login_finished.emit(status, LoginStatus)
        scrape_thread_event.set()

    def run_scrapp_thread(
        self, loop, browser, page, json_data_str, output_text, scrape_thread_event
    ):
        asyncio.set_event_loop(loop)
        status, scrapping_status = loop.run_until_complete(
            scrapping_data(browser, page, json_data_str, output_text)
        )
        self.scrapping_finished.emit(status, scrapping_status)
        scrape_thread_event.set()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(500, 600, 800, 500)
        center_window(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        app_title_label = QLabel(f"<h1>{APP_NAME}</h1>")
        app_title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(app_title_label)
        
        font = QFont()
        font.setBold(True)
        
        form_layout = QVBoxLayout()
        form_layout.addSpacing(20)
        layout.addLayout(form_layout)
        
        form_layout.addWidget(QLabel("<b>Enter the username and email address:</b>"))
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("Enter the username and email address")
        self.username_field.setFont(font)
        self.username_field.setStyleSheet("height: 20px;")
        form_layout.addWidget(self.username_field)
        
        form_layout.addWidget(QLabel("<b>Enter the password:</b>"))
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setStyleSheet("height: 20px;")
        self.password_field.setPlaceholderText("Enter the password")
        self.password_field.setFont(font)
        form_layout.addWidget(self.password_field)

        button_layout = QHBoxLayout()
        form_layout.addLayout(button_layout)
        
        self.login_button = QPushButton("Login")
        self.login_button.setFont(font)
        self.login_button.clicked.connect(self.login_function)
        button_layout.addWidget(self.login_button)

        self.close_button = QPushButton("Close Window")
        self.close_button.clicked.connect(self.closed_window)
        self.close_button.setFont(font)
        button_layout.addWidget(self.close_button)

        bottom_button_layout = QHBoxLayout()
        layout.addLayout(bottom_button_layout)

        self.upload_csv_button = QPushButton("Upload Excel File")
        self.upload_csv_button.setEnabled(False)
        self.upload_csv_button.clicked.connect(self.upload_excel)
        self.upload_csv_button.setFont(font)
        bottom_button_layout.addWidget(self.upload_csv_button)

        self.scrap_data_button = QPushButton("Scrap Data")
        self.scrap_data_button.setEnabled(False)
        self.scrap_data_button.clicked.connect(self.scrap_data_button_clicked)
        self.scrap_data_button.setFont(font)
        bottom_button_layout.addWidget(self.scrap_data_button)

        layout.addWidget(QLabel("<b>Output:</b>"))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Arial", 12))
        layout.addWidget(self.output_text)

    def login_function(self):
        username = self.username_field.text()
        password = self.password_field.text()

        self.login_button.setEnabled(False)
        self.upload_csv_button.setEnabled(False)
        self.scrap_data_button.setEnabled(False)

        if username == "" or password == "":
            show_message_box(
                self,
                QMessageBox.Warning,
                "Validation Error",
                "Please enter the username and password",
            )
            self.login_button.setEnabled(True)
        else:
            global browser
            browser = pyppeteerBrowserInit(NEW_EVENT_LOOP)

            self.worker = Worker()
            self.worker.login_finished.connect(self.on_login_finished)

            scrape_thread = Thread(
                target=self.worker.run_login_thread,
                args=(
                    NEW_EVENT_LOOP,
                    browser,
                    username,
                    password,
                    self.output_text,
                    THREAD_EVENT,
                ),
            )
            scrape_thread.start()

    def on_login_finished(self, status, LoginStatus):
        if status:
            print_the_output_statement(self.output_text, LoginStatus)
            self.upload_csv_button.setEnabled(True)
        else:
            show_message_box(self, QMessageBox.Warning, "Browser Error", LoginStatus)
            self.login_button.setEnabled(True)

    def upload_excel(self):
        print_the_output_statement(self.output_text, f"Uploading Excel...")
        options = QFileDialog.Options()
        global file_path
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File Name", "", "Excel Files (*.xlsx)", options=options
        )
        if file_path:
            self.file_path = file_path
            self.scrap_data_button.setEnabled(True)
            self.login_button.setEnabled(False)
            self.upload_csv_button.setEnabled(False)
            print_the_output_statement(
                self.output_text, f"excel  file selected {file_path}"
            )
        else:
            show_message_box(
                self,
                QMessageBox.Warning,
                "File Error",
                "Please Choose the Correct Excel  File",
            )

    def on_scrapping_finished(self, status, scrapping_status):
        if status:
            print_the_output_statement(self.output_text, f"Scraping completed.")
            # print('scrapping_status', scrapping_status)

            options = QFileDialog.Options(    )
            folder_path = QFileDialog.getExistingDirectory(
                self, "Select Directory", options=options
            )
            if folder_path:
                reformatted = reformat_data(scrapping_status)
                # print('reformatted', reformatted)
                outputfile = f"{folder_path}/{FILE_NAME}_generate_report_{CURRENT_DATE.strftime('%Y-%B-%d')}.{FILE_TYPE}"
                print("outputfile", outputfile)
                convert_into_csv_and_save(reformatted, outputfile)
                print_the_output_statement(
                    self.output_text, f"Data saved successfully to {outputfile}"
                )
                show_message_box(
                    self,
                    QMessageBox.NoIcon,
                    "success",
                    f"Data saved successfully to {outputfile}",
                )
            else:
                show_message_box(
                    self,
                    QMessageBox.Warning,
                    "error",
                    "data successfully found succssfully but failed to the saved the data",
                )
            self.upload_csv_button.setEnabled(False)
            self.scrap_data_button.setEnabled(False)
            self.login_button.setEnabled(True)
        else:
            show_message_box(
                self,
                QMessageBox.Warning,
                "Browser Error",
                "Internal Error Occurred while running application. Please Try Again!!",
            )
        self.login_button.setEnabled(True)
        end_time = time.time()
        total_time = end_time - START_TIME
        print_the_output_statement(
            self.output_text,
            f"Total execution time for Scrapping : {total_time:.2f} seconds",
        )

    def scrap_data_button_clicked(self):
        print_the_output_statement(
            self.output_text, "Scrapping started, please wait for few minutes."
        )
        self.scrap_data_button.setEnabled(False)
        if file_path:
            csv_header, json_data_str, num_records = xlsx_to_json(file_path)
            print('json_data_str', )
            if num_records > 0:
                print("json data is found")
                # Missing Headers
                missing_headers = [
                    header
                    for header in ["Server_ID", "Last_Name"]
                    if header not in csv_header
                ]
                if missing_headers:
                    print("missing the headers ")
                    self.upload_csv_button.setEnabled(True)
                    self.scrap_data_button.setEnabled(False)
                    show_message_box(
                        self,
                        QMessageBox.Warning,
                        "File Error",
                        "missing the header in the csv please choose the correct excel file",
                    )
                else:
                    print("missing the headers ")
                    self.worker = Worker()
                    self.worker.scrapping_finished.connect(self.on_scrapping_finished)
                    scrape_thread = Thread(
                        target=self.worker.run_scrapp_thread,
                        args=(
                            NEW_EVENT_LOOP,
                            browser,
                            page,
                            json_data_str,
                            self.output_text,
                            THREAD_EVENT,
                        ),
                    )
                    scrape_thread.start()
                

            else:
                self.upload_csv_button.setEnabled(True)
                self.scrap_data_button.setEnabled(False)
                print("json data is not Found")
                show_message_box(
                    self,
                    QMessageBox.Warning,
                    "File Error",
                    "Excel is empty please choose another Excel sheet",
                )
            # self.worker.scrapping_finished.connect(self.on_scrapping_finished)

            # scrape_thread = Thread(
            #     target=self.worker.run_scrapp_thread,
            #     args=(
            #         NEW_EVENT_LOOP,
            #         browser,
            #         page,
            #         json_data_str,
            #         self.output_text,
            #         THREAD_EVENT,
            #     ),
            # )
            # scrape_thread.start()
        else:
            show_message_box(self, QMessageBox.Warning, "File Error", "File not found.")

    def closed_window(self):
        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure you want to close the window?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.browser_cleanup()
            self.close()

    def closeEvent(self, event):
        self.browser_cleanup()
        event.accept()

    def browser_cleanup(self):
        if "browser" in globals() and browser:
            asyncio.ensure_future(self.close_browser())
        else:
            QCoreApplication.quit()

    async def close_browser(self):
        await browser.close()
        print("Browser instance closed")
        QCoreApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(bootstrap_style)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
