import face_recognition
from PIL import UnidentifiedImageError
from PyQt5.QtCore import QThread, pyqtSignal
import os
from .utility import alphabetized_name, move_img, percent_complete, load_dict, load_and_convert, auto_rotate_image, \
    convert_and_write


class CreateFaceDictThread(QThread):
    progress_updated = pyqtSignal(int)

    def __init__(self, known_dict, total):
        super().__init__()
        self.known_dict = known_dict
        self.total = total

    def run(self):
        if os.path.isfile('known_faces.json'):
            known_dict_list = load_dict()
        else:
            known_dict_list = []
        no_face_list = []
        file_count = 0
        file_count_total = self.total
        for dict in self.known_dict:
            for key, values in dict.items():
                image_encoding = []
                for image_path in values:
                    auto_rotate_image(image_path)
                    known_face = face_recognition.load_image_file(image_path)
                    try:
                        known_face_encoding = face_recognition.face_encodings(known_face)[0]
                    except IndexError:
                        no_face_list.append(image_path)
                        continue
                    known_face_encoding_list = known_face_encoding.tolist()
                    image_encoding.append(known_face_encoding_list)
                    file_count += 1
                    percent = percent_complete(file_count_total, file_count)
                    self.progress_updated.emit(percent)
                known_dict = {'name': f'{key}', 'encoding': image_encoding}
                known_dict_list.append(known_dict)
            convert_and_write(known_dict_list)


class IdentifyThread(QThread):
    progress_updated = pyqtSignal(int)

    def __init__(self, folders, output_folder, total):
        super().__init__()
        self.folders = folders
        self.output = output_folder
        self.total = total

    def run(self):
        file_count = 0
        data = load_and_convert()
        for folder in self.folders:
            for picture in os.listdir(folder):
                found_face = []
                img_path = os.path.join(folder, picture)
                try:
                    auto_rotate_image(img_path)
                except (UnidentifiedImageError, PermissionError):
                    continue
                unknown_face = face_recognition.load_image_file(img_path)
                unknown_face_encodings = face_recognition.face_encodings(unknown_face)
                for face in unknown_face_encodings:
                    next_face = False
                    for known_dict in data:
                        for encoding_data in known_dict['encoding']:
                            skip_person = False
                            for name in found_face:
                                if known_dict['name'] == name:
                                    skip_person = True
                            if skip_person:
                                continue
                            results = face_recognition.compare_faces([encoding_data], face, tolerance=.53)

                            if results[0]:
                                next_face = True
                                found_face.append(known_dict['name'])
                                break
                        if next_face:
                            break

                if len(found_face) == 0:
                    sorted_name = 'unknown'
                else:
                    sorted_name = alphabetized_name(found_face)
                move_img(self.output, sorted_name, img_path)
                file_count += 1
                percent = percent_complete(self.total, file_count)
                self.progress_updated.emit(percent)
