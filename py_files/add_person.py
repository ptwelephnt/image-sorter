from os import path
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QPushButton, QWidget, QLineEdit, QLabel, QFileDialog
from PyQt5.uic import loadUi

from .utility import set_gradient


class AddKnownFace(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(320, 282)
        self.setWindowTitle('Add Person')
        self.setAttribute(Qt.WA_DeleteOnClose)

        set_gradient(self)

        self.parent = parent

        self.image_list = []

        self.header = QLabel(self)
        self.header.setGeometry(QRect(16, 13, 291, 31))
        font = QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setText("Add Name and Picture(s)")

        self.sub_header = QLabel(self)
        self.sub_header.setGeometry(QRect(6, 43, 301, 21))
        font.setPointSize(10)
        self.sub_header.setFont(font)
        self.sub_header.setAlignment(Qt.AlignCenter)
        self.sub_header.setText("Only one or two pictures are necessary")

        self.name_line = QLineEdit(self)
        self.name_line.setGeometry(QRect(100, 80, 121, 20))
        font = QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.name_line.setFont(font)
        self.name_line.setAlignment(Qt.AlignCenter)
        self.name_line.setPlaceholderText("Person's Name")

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QRect(10, 110, 301, 101))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.pic_layout = QHBoxLayout(self.horizontalLayoutWidget)
        self.pic_layout.setContentsMargins(0, 0, 0, 0)
        self.pic_layout.setObjectName("pic_layout")

        self.horizontalLayoutWidget_2 = QWidget(self)
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 220, 301, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.buttons_layout = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setObjectName("buttons_layout")

        self.add_button_layout = QHBoxLayout()
        self.add_button_layout.setContentsMargins(20, -1, 20, -1)
        self.add_button_layout.setObjectName("add_button_layout")
        self.add_button = QPushButton(self.horizontalLayoutWidget_2)
        font.setPointSize(8)
        self.add_button.setFont(font)
        self.add_button.setText("Add Image")
        self.add_button.clicked.connect(self.add_image)
        self.add_button_layout.addWidget(self.add_button)
        self.buttons_layout.addLayout(self.add_button_layout)

        self.done_button_layout = QHBoxLayout()
        self.done_button_layout.setContentsMargins(20, -1, 20, -1)
        self.done_button_layout.setObjectName("done_button_layout")
        self.done_button = QPushButton(self.horizontalLayoutWidget_2)
        self.done_button.setFont(font)
        self.done_button.setText("Done")
        self.done_button.clicked.connect(self.done_clicked)
        self.done_button_layout.addWidget(self.done_button)
        self.buttons_layout.addLayout(self.done_button_layout)

        self.show()

    def add_image(self):
        image = QFileDialog.getOpenFileName(self, 'Select Images', '/', 'Images (*.png *.jpg *.apng *.gif '
                                                                          '*.ico *.cur *.jpeg *.jfif *.pjpeg'
                                                                          ' *.pjp *.svg)')
        if image[0]:
            self.image_list.append(image[0])
            image_label = QLabel(self)
            pixmap = QPixmap(image[0]).scaled(75, 75, aspectRatioMode=Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            self.pic_layout.addWidget(image_label, alignment=Qt.AlignCenter)

    def done_clicked(self):
        name = self.name_line.text()
        if name and len(self.image_list) != 0:
            self.parent.add_item(name, path_list=self.image_list)
            self.close()
        else:
            fix_dialog = QDialog(self)
            fix_dialog.setAttribute(Qt.WA_DeleteOnClose)
            set_gradient(fix_dialog)
            parent_directory = path.dirname(path.dirname(__file__))
            path_to_fix_required_ui = path.abspath(path.join(parent_directory, 'ui/fix_required.ui'))
            loadUi(path_to_fix_required_ui, fix_dialog)
            fix_dialog.pushButton.clicked.connect(fix_dialog.close)
            if name == '' and len(self.image_list) != 0:
                fix_dialog.label.setText('Please add Name')
            elif name != '' and len(self.image_list) == 0:
                fix_dialog.label.setText('Please add an image')
            fix_dialog.show()
