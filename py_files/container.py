from os import path
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog, QDialog
from PyQt5.uic import loadUi
from .known_table_widget import KnownFaceTable
from .utility import set_font, set_gradient
from .output_button import OutputButton


class GenericWidget(QWidget):
    def __init__(self, parent=None, window=0):
        super(GenericWidget, self).__init__(parent=parent)
        self.parent = parent
        parent_width = self.parent.width()
        self.resize(400, 450)
        self.window = window
        self.font = set_font()
        self.font.setPointSize(18)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 22, parent_width, 41))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(self.font)

        self.font.setPointSize(8)

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QRect(0, 390, parent_width, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.button_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.button_layout.setContentsMargins(20, 0, 20, 0)
        self.button_layout.setObjectName("button_layout")

        self.back_layout = QVBoxLayout()
        self.back_layout.setContentsMargins(20, 0, 20, 0)
        self.back_layout.setObjectName("back_layout")

        self.back_button = QPushButton(self.horizontalLayoutWidget)
        self.back_button.setText('Back')
        self.back_button.setFont(self.font)
        self.back_button.clicked.connect(self.go_back)
        self.back_layout.addWidget(self.back_button)
        self.button_layout.addLayout(self.back_layout)

        self.next_layout = QVBoxLayout()
        self.next_layout.setContentsMargins(20, 0, 20, 0)
        self.next_layout.setObjectName("next_layout")

        self.next_button = QPushButton(self.horizontalLayoutWidget)
        self.next_button.setText('Next')
        self.next_button.setFont(self.font)
        self.next_button.clicked.connect(self.next)
        self.next_layout.addWidget(self.next_button)
        self.button_layout.addLayout(self.next_layout)

        self.grab_widget()

        self.show()

    def grab_widget(self):
        self.window += 1
        self.widget = KnownFaceTable(self.window, self)
        self.label.setText(self.widget.parent_header)
        self.widget.setGeometry(QRect(0, 70, self.widget.width(), self.widget.height()))

    def select_output_ui(self):
        self.window += 1
        self.widget.deleteLater()
        self.label.setText('Choose Output Folder')
        self.widget = OutputButton(self)
        self.widget.setGeometry(QRect(0, 70, self.widget.width(), self.widget.height()))
        self.widget.output_button.clicked.connect(self.choose_output_directory)

    def choose_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", "/")

        if directory:
            folder_path = directory.split('/')
            folder = folder_path[-1]
            self.widget.output_button.setText(folder)
            self.parent.output = directory

    def go_back(self):
        if self.window == 1:
            self.parent.start_menu()
        elif self.window == 2:
            self.window -= 2
            self.widget.deleteLater()
            self.grab_widget()
        elif self.window == 3:
            self.window -= 2
            self.widget.deleteLater()
            self.grab_widget()

    def next(self):
        if self.window == 1:
            self.parent.known_faces = self.widget.faces_list
            self.parent.faces_total = self.widget.faces_total
            self.widget.deleteLater()
            self.grab_widget()
        elif self.window == 2:
            self.parent.folders = self.widget.to_be_sorted
            self.parent.img_total = self.widget.to_be_total
            if self.parent.img_total == 0:
                fix_dialog = QDialog(self)
                fix_dialog.setAttribute(Qt.WA_DeleteOnClose)
                parent_directory = path.dirname(path.dirname(__file__))
                path_to_fix_required_ui = path.abspath(path.join(parent_directory, 'ui/fix_required.ui'))
                loadUi(path_to_fix_required_ui, fix_dialog)
                set_gradient(fix_dialog)
                fix_dialog.label.setText('No Images to sort')
                fix_dialog.pushButton.clicked.connect(fix_dialog.close)
                fix_dialog.show()
            else:
                self.widget.deleteLater()
                self.select_output_ui()
        elif self.window == 3:

            self.parent.confirmation()
