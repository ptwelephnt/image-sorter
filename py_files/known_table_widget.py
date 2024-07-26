import os
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QFileDialog
from .add_person import AddKnownFace
from .utility import set_font


class KnownFaceTable(QWidget):
    def __init__(self, window, parent=None):
        super(KnownFaceTable, self).__init__(parent=parent)
        self.resize(395, 305)

        self.font = set_font()

        self.faces_list = []
        self.faces_total = 0
        self.to_be_sorted = []
        self.to_be_total = 0
        self.new_person = None

        self.known_faces_table = QTableWidget(self)
        self.known_faces_table.setGeometry(QRect(10, 10, 375, 231))
        self.known_faces_table.setMinimumSize(QSize(360, 231))
        self.known_faces_table.setColumnCount(3)
        self.known_faces_table.setColumnWidth(0, 150)
        self.known_faces_table.setColumnWidth(1, 100)
        self.known_faces_table.setColumnWidth(2, 100)
        self.known_faces_table.verticalHeader().hide()
        self.known_faces_table.horizontalHeader().setStretchLastSection(True)

        self.known_faces_table.setObjectName("known_faces_table")
        self.known_faces_table.setRowCount(0)

        self.item0 = QTableWidgetItem()
        self.item0.setFont(self.font)
        self.known_faces_table.setHorizontalHeaderItem(0, self.item0)

        self.item1 = QTableWidgetItem()
        self.item1.setText('Image(s)')
        self.item1.setFont(self.font)
        self.known_faces_table.setHorizontalHeaderItem(1, self.item1)

        self.item2 = QTableWidgetItem()
        self.item2.setText('Delete')
        self.item2.setFont(self.font)
        self.known_faces_table.setHorizontalHeaderItem(2, self.item2)

        self.horizontalLayoutWidget_3 = QWidget(self)
        self.horizontalLayoutWidget_3.setGeometry(QRect(234, 250, 146, 49))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.add_person_layout = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.add_person_layout.setContentsMargins(20, 0, 20, 0)

        self.add_person = QPushButton(self.horizontalLayoutWidget_3)
        self.add_person.setFont(self.font)
        self.add_person_layout.addWidget(self.add_person)

        if window == 1:
            self.parent_header = 'Choose Known Faces'
            self.item0.setText('Name')
            self.add_person.setText("Add Person")
            self.add_person.clicked.connect(self.call_person_dialog)
        if window == 2:
            self.parent_header = 'Choose Folders to Sort'
            self.item0.setText('Folder')
            self.add_person.setText("Add Folder")
            self.add_person.clicked.connect(self.choose_to_be_sorted)

        self.show()

    def call_person_dialog(self):
        self.add_dialog = AddKnownFace(self)

    def choose_to_be_sorted(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory to Sort", "/")
        if directory:
            self.to_be_sorted.append(directory)
            folder_path = directory.split('/')
            folder_name = folder_path[-1]
            num_images = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
            no_images = self.add_item(folder_name, num_images=num_images)
            if no_images:
                pass

    def add_item(self, name, path_list=None, num_images=None):
        row = self.known_faces_table.rowCount()
        self.known_faces_table.setRowCount(row + 1)
        row_name = QTableWidgetItem(name)
        row_name.setTextAlignment(Qt.AlignCenter)
        self.known_faces_table.setItem(row, 0, row_name)

        if path_list:
            self.faces_list.append({name: path_list})
            number_of_images = len(path_list)
            self.faces_total += number_of_images
        elif num_images:
            number_of_images = num_images
            self.to_be_total += number_of_images
        else:
            return True

        item_number_imgs = QTableWidgetItem(f'{number_of_images}')
        item_number_imgs.setTextAlignment(Qt.AlignCenter)
        item_number_imgs.setFont(self.font)

        button = QPushButton('Delete')
        button.setFont(self.font)
        button.clicked.connect(self.delete_row)
        button_widget = QTableWidgetItem()
        button_widget.setTextAlignment(Qt.AlignCenter)

        self.known_faces_table.setItem(row, 1, item_number_imgs)
        self.known_faces_table.setItem(row, 2, button_widget)
        self.known_faces_table.setCellWidget(row, 2, button)
        return False

    def delete_row(self):
        button = self.sender()
        if button:
            item_index = self.known_faces_table.indexAt(button.pos())
            row = item_index.row()
            name_item = self.known_faces_table.item(row, 0)
            number_item = self.known_faces_table.item(row, 1)
            number = int(number_item.text())
            if self.parent_header == 'Choose Known Faces':
                self.remove_dict(name_item.text())
                self.faces_total -= number
            elif self.parent_header == 'Choose Folders to Sort':
                self.to_be_sorted.pop(row)
                self.to_be_total -= number
            self.known_faces_table.removeRow(row)

    def remove_dict(self, name):
        for i, person_dict in enumerate(self.faces_list):
            if name in person_dict:
                self.faces_list.pop(i)
