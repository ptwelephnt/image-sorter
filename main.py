import os
import sys
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QApplication, QDialog
from PyQt5.uic import loadUi
from py_files.container import GenericWidget
from py_files.utility import set_gradient
from py_files.start_menu import StartMenu
from py_files.threads import CreateFaceDictThread, IdentifyThread

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sort = None
        self.create_known_dict = None
        self.progress = None
        self.container = None
        self.confirm_dialog = None
        self.known_faces = None
        self.faces_total = None
        self.folders = None
        self.img_total = None
        self.output = None
        self.loaded = False
        self.bundle_dir = os.path.dirname(__file__)

        path_to_main_window_ui = os.path.abspath(os.path.join(self.bundle_dir, 'ui/MainWindow.ui'))
        loadUi(path_to_main_window_ui, self)
        self.setWindowTitle('ImageSorter')
        set_gradient(self)

        self.main_layout = QHBoxLayout()
        self.centralWidget().setLayout(self.main_layout)
        self.start_menu()

    def start_menu(self):
        if self.container:
            self.container.close()
        self.start = StartMenu(self)

    def set_container(self, window=0):
        self.start.close()
        self.container = GenericWidget(self, window)
        width = self.width()
        container_width = self.container.width()
        margin = int((width - container_width) / 2)
        self.container.setGeometry(QRect(margin, 0, self.container.width(), self.container.height()))
        self.main_layout.addWidget(self.container, alignment=Qt.AlignCenter)

    def confirmation(self):
        self.confirm_dialog = QDialog(self)
        set_gradient(self.confirm_dialog)
        self.confirm_dialog.setAttribute(Qt.WA_DeleteOnClose)
        path_to_confirmation_ui = os.path.abspath(os.path.join(self.bundle_dir, 'ui/confirmation.ui'))
        loadUi(path_to_confirmation_ui, self.confirm_dialog)
        self.confirm_dialog.go_back_button.clicked.connect(self.close_confirm)
        if not self.loaded:
            self.confirm_dialog.start_button.clicked.connect(self.start_sorting)
        elif self.loaded:
            self.confirm_dialog.start_button.clicked.connect(self.start_sorting2)
        self.confirm_dialog.show()

    def close_confirm(self):
        self.confirm_dialog.close()

    def start_sorting(self):
        self.hide()
        self.confirm_dialog.close()
        self.progress_dialog()
        self.progress.label.setText('Creating Known Faces Dictionary...')
        self.progress.label.adjustSize()
        self.progress.adjustSize()
        self.create_known_dict = CreateFaceDictThread(self.known_faces, self.faces_total)
        self.create_known_dict.progress_updated.connect(self.update_progress)
        self.create_known_dict.finished.connect(self.end_create_face)
        self.create_known_dict.start()

    def end_create_face(self):
        self.progress.close()
        self.start_sorting2()

    def start_sorting2(self):
        self.hide()
        if self.loaded:
            self.confirm_dialog.close()
        self.progress_dialog()
        self.progress.label.setText('Sorting Pictures...')
        self.sort = IdentifyThread(self.folders, self.output, self.img_total)
        self.sort.progress_updated.connect(self.update_progress)
        self.sort.finished.connect(self.finished)
        self.sort.start()

    def progress_dialog(self):
        self.progress = QDialog(self)
        set_gradient(self.progress)
        self.progress.setAttribute(Qt.WA_DeleteOnClose)
        path_to_progress_ui = os.path.abspath(os.path.join(self.bundle_dir, 'ui/progress_bar.ui'))
        loadUi(path_to_progress_ui, self.progress)
        self.progress.progressBar.setValue(0)
        self.progress.show()
        
    def update_progress(self, percentage):
        self.progress.progressBar.setValue(percentage)

    def finished(self):
        self.progress.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
