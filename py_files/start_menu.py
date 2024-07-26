import os.path
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel
from .utility import set_font, KNOWN_FACES_PATH


class StartMenu(QWidget):
    def __init__(self, parent):
        super(StartMenu, self).__init__(parent=parent)
        self.parent = parent
        parent_width = self.parent.width()
        self.font = set_font()
        self.font.setPointSize(18)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(16, 22, parent_width, 41))
        self.label.setText('ImageSorter')
        self.label.setFont(self.font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setGeometry(QRect(0, 80, parent_width, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(100, 0, 100, 0)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.font.setPointSize(12)
        self.pushButton.setFont(self.font)
        self.pushButton.setText('New Game')
        self.pushButton.clicked.connect(self.new_game)
        self.verticalLayout.addWidget(self.pushButton)

        if os.path.isfile(KNOWN_FACES_PATH):
            self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
            self.pushButton_2.setFont(self.font)
            self.pushButton_2.setText('Load Save')
            self.pushButton_2.clicked.connect(self.load_save)
            self.verticalLayout.addWidget(self.pushButton_2)

        self.adjustSize()

        self.show()

    def new_game(self):
        self.parent.set_container()

    def load_save(self):
        self.parent.loaded = True
        self.parent.set_container(1)
