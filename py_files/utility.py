import json
import numpy as np
from PIL import Image
import os
import shutil
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QLinearGradient, QColor, QBrush, QPalette
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton

BUNDLE_DIR = os.path.dirname(os.path.dirname(__file__))
KNOWN_FACES_PATH = os.path.abspath(os.path.join(BUNDLE_DIR, 'json/known_faces.json'))

def set_font():
    font = QFont()
    font.setFamily("Segoe UI Semibold")
    font.setBold(True)
    font.setWeight(75)
    return font

def load_dict():

    with open(KNOWN_FACES_PATH, 'r') as file:
        data = json.load(file)
        return data

def load_and_convert():
    data = load_dict()
    for face in data:
        face['encoding'] = [np.array(encoding) for encoding in face['encoding']]
    return data


def convert_and_write(known_dict_list):
    with open(KNOWN_FACES_PATH, 'w') as file:
        json.dump(known_dict_list, file, indent=2)


def auto_rotate_image(file_path):
    with Image.open(file_path) as img:
        try:
            # Get EXIF orientation data
            exif = img._getexif()
            if exif is not None:
                exif_orientation = exif.get(0x0112)
                if exif_orientation == 3:
                    img = img.rotate(180, expand=True)
                elif exif_orientation == 6:
                    img = img.rotate(270, expand=True)
                elif exif_orientation == 8:
                    img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # No EXIF data or orientation data is missing
            print(f'No exif or orientation data for {file_path}')

        # Save the rotated image
        img.save(file_path)

def check_for_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def move_img(output_folder, name, og_image_path):
    file_name = os.path.split(og_image_path)[1]
    person_folder = os.path.join(output_folder, name)
    check_for_directory(person_folder)
    
    target_path = os.path.join(person_folder, file_name)
    if os.path.exists(target_path):
        person_folder = os.path.join(person_folder, 'duplicates')
        check_for_directory(person_folder)

    shutil.move(og_image_path, person_folder)


def copy_img(output_folder, name, og_image_path):
    person_folder = os.path.join(output_folder, name)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)

    shutil.copy(og_image_path, person_folder)


def get_total(directory_list):
    total = 0
    for directory in directory_list:
        for image in os.listdir(directory):
            total += 1
    return total


def get_total2(directory):
    total = 0
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        for image in os.listdir(folder_path):
            total += 1
    return total


def percent_complete(total_pictures, current_picture):
    percent = int(100 * float(current_picture) / float(total_pictures))
    return percent


def alphabetized_name(name_list):
    sorted_name_list = sorted(name_list)
    full_name = ''
    for name in sorted_name_list:
        full_name += f'{name} '
    full_name = full_name[:-1]
    return full_name


def write_readme(base_dir, folder, match_info):
    person_folder = os.path.join(base_dir, folder)
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    readme_path = os.path.join(person_folder, 'readme.txt')
    if os.path.isfile(readme_path):
        mode = 'a'
    else:
        mode = 'w'
    with open(readme_path, mode) as file:
        for text in match_info:
            file.write(text)
            file.write('\n')
        file.write('----------------\n')


def move_back(start_directory, end_directory):
    for folder in os.listdir(start_directory):
        folder_path = os.path.join(start_directory, folder)
        for image in os.listdir(folder_path):
            current_location = os.path.join(folder_path, image)
            final_destination = os.path.join(end_directory, image)
            shutil.move(current_location, final_destination)


def delete_layout(layout):
    while layout.count():  # while there are items in the layout
        item = layout.takeAt(0)  # take the first item
        widget = item.widget()  # get the widget from the item
        if widget is not None:  # if there is a widget
            widget.deleteLater()  # delete the widget
        else:
            sublayout = item.layout()  # get the sub-layout from the item
            if sublayout is not None:  # if there is a sub-layout
                while sublayout.count():  # while there are items in the sub-layout
                    subitem = sublayout.takeAt(0)  # take the first item
                    subwidget = subitem.widget()  # get the widget from the item
                    if subwidget is not None:  # if there is a widget
                        subwidget.deleteLater()


def create_labels(parent, dictionary, layout):
    label_list = []
    for each in dictionary:
        label = QLabel(parent)
        label.setText(each[0])
        label.setFont(QFont('Segoe UI Variable Text Semibold', 18))
        layout.addWidget(label, alignment=Qt.AlignCenter)
        label_list.append(label)
    return label_list


def create_line_edits(parent, dictionary, layout):
    line_list = []
    for each in dictionary:
        line = QLineEdit(parent)
        line.setPlaceholderText(each[0])
        line.setAlignment(Qt.AlignCenter)
        line.setFont(QFont('Segoe UI Variable Text Semibold', 10))
        layout.addWidget(line, Qt.AlignCenter)
        line_list.append(line)
    return line_list


def create_buttons(parent, dictionary, layout):
    buttons_list = []
    for each in dictionary:
        button = QPushButton(parent)
        button.setText(each[0])
        button.setMinimumSize(150, 50)
        button.setFont(QFont('Segoe UI Variable Text Semibold', 10))
        layout.addWidget(button, alignment=Qt.AlignCenter)
        buttons_list.append(button)
    return buttons_list


def delete_widgets(widget_layout, widget_list):
    for widget in widget_list:
        widget_layout.removeWidget(widget)
        widget.deleteLater()


def set_gradient(widget):
    gradient = QLinearGradient(0, 0, 0, widget.height())
    gradient.setColorAt(0.0, QColor(0, 0, 255))
    gradient.setColorAt(1.0, QColor(0, 175, 255))
    brush = QBrush(gradient)

    widget.palette = QPalette()
    widget.palette.setBrush(QPalette.Background, brush)
    widget.setPalette(widget.palette)
