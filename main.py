"""
Python 3.12 Program Console Block (Text Writer)
Update main.py file

Version: 0.0.1
Author: Nicolas Dias
Date: 23/07/2024
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QVBoxLayout, QWidget, QPlainTextEdit, QFileDialog, QToolBar, QStatusBar, QMessageBox
)
from PyQt6.QtGui import QAction, QIcon, QCloseEvent
from PyQt6.QtCore import QSize
from PyQt6.QtPrintSupport import QPrintDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("UnicodePad")
        self.setWindowIcon(QIcon("./icons/notepad.png"))

        self.path = None

        # Create a central widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Create the main vertical layout
        mainLayout = QVBoxLayout(centralWidget)

        # Create and add the text editor to the main layout
        self.editor = QPlainTextEdit(self)
        mainLayout.addWidget(self.editor)

        # File toolbar
        file_toolbar = QToolBar()
        file_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(file_toolbar)
        file_toolbar.addSeparator()

        # Edit Toolbar
        edit_toolbar = QToolBar()
        edit_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(edit_toolbar)

        self.setStatusBar(QStatusBar(self))
        menu = self.menuBar()

        filemenu = menu.addMenu("&File")
        editmenu = menu.addMenu("&Edit")

        # New File, Open File, save, saveAS, print
        new_file = self.create_action(
            self,
            "./icons/plus.png",
            "New File",
            "New file",
            "ctrl+shift+n",
            self.new_file
        )
        open_file = self.create_action(
            self,
            "./icons/document-text.png",
            "Open",
            "Open file",
            "ctrl+n",
            self.open
        )
        file_save = self.create_action(
            self,
            "./icons/disk.png",
            "save",
            "save file",
            "ctrl+s",
            self.save
        )

        file_saveas = self.create_action(
            self,
            "./icons/disk--arrow.png",
            "save as",
            "save file as",
            "ctrl+shift+s",
            self.saveas
        )
        file_print = self.create_action(
            self,
            "./icons/printer-color.png",
            "Print",
            "Print",
            "ctrl+p",
            self.print
        )
        filemenu.addActions([new_file, open_file, file_save, file_saveas, file_print])
        file_toolbar.addActions([new_file, open_file, file_save, file_saveas, file_print])

        # Undo, redo, clear, cut, copy, paste, select all

        undo_action = self.create_action(
            self,
            "./icons/arrow-curve-180-left.png",
            "Undo",
            "Undo",
            "ctrl+z",
            self.editor.undo
        )
        redo_action = self.create_action(
            self,
            "./icons/arrow-curve.png",
            "Redo",
            "Redo",
            "ctrl+y",
            self.editor.redo
        )
        cut_text = self.create_action(
            self,
            "./icons/scissors.png",
            "Cut",
            "Cut selected text",
            "ctrl+x",
            self.editor.cut
        )
        copy_text = self.create_action(
            self,
            "./icons/document-copy.png",
            "Copy",
            "Copy selected text",
            "ctrl+c",
            self.editor.copy
        )
        paste_text = self.create_action(
            self,
            "./icons/document-import.png",
            "Paste",
            "Paste the text from clipboard",
            "ctrl+v",
            self.editor.paste
        )
        select_all = self.create_action(
            self,
            "./icons/document-tex.png",
            "Select All",
            "Select all the text",
            "ctrl+a",
            self.editor.selectAll
        )
        editmenu.addActions([undo_action, redo_action, cut_text, copy_text, paste_text, select_all])
        edit_toolbar.addActions([undo_action, redo_action, cut_text, copy_text, paste_text, select_all])

    def create_action(

            self, parent, icon, action_name, status_tip, shortcut, trigger
    ):
        action = QAction(QIcon(icon), action_name, parent)
        action.setStatusTip(status_tip)
        action.triggered.connect(trigger)
        action.setShortcut(shortcut)
        return action

    def save(self):
        if self.path is None:
            self.saveas()
        else:
            try:
                with open(self.path, 'w') as f:
                    f.write(self.editor.toPlainText())
                    self.dialog_message("File saved successfully", QMessageBox.Icon.Information, "Success")
            except Exception as e:
                self.dialog_message(str(e), QMessageBox.Icon.Critical, "Error")

    def saveas(self):
        dialog = QFileDialog(self)
        if dialog.exec():
            try:
                fileLocation = dialog.selectedFiles()[0]
                with open(fileLocation, 'w') as f:
                    f.write(self.editor.toPlainText())
                    self.dialog_message(f"File created successfully at {fileLocation}", QMessageBox.Icon.Information,
                                        "Success")
                self.path = fileLocation
            except Exception as e:
                self.dialog_message(str(e), QMessageBox.Icon.Critical, "Error")

    def dialog_message(self, message, icon_type, title):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        dlg.setIcon(icon_type)
        dlg.exec()

    def new_file(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Create New File")

        if dialog.exec():
            try:
                fileLocation = dialog.selectedFiles()[0]
                with open(fileLocation, 'w') as f:
                    f.write("")
                    with open(fileLocation, 'r') as file:
                        text = file.read()
                        self.editor.setPlainText(text)
                    self.dialog_message(f"File created successfully", QMessageBox.Icon.Information, "Success")
                self.path = fileLocation
            except Exception as e:
                self.dialog_message(str(e), QMessageBox.Icon.Critical)

    def open(self):
        dialog = QFileDialog(self)
        if dialog.exec():
            try:
                fileLocation = dialog.selectedFiles()[0]
                with open(fileLocation, 'r') as f:
                    text = f.read()
                    self.editor.setPlainText(text)
                    self.dialog_message(f"File opened successfully", QMessageBox.Icon.Information, "Success")
                self.path = fileLocation
            except Exception as e:
                self.dialog_message(str(e), QMessageBox.Icon.Critical)

    def print(self):
        printDlg = QPrintDialog()
        if printDlg.exec():
            self.editor.print(printDlg.printer())
        pass

    def closeEvent(self, event):
        if self.path is not None:
            event.accept()
        else:
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "Want to exit without save?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Save |
                QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save()
            elif reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
