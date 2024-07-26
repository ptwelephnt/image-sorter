from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class OutputButton(QWidget):
    def __init__(self, parent=None):
        super(OutputButton, self).__init__(parent=parent)
        self.resize(395, 305)

        self.layout = QHBoxLayout(self)
        self.layout.setGeometry(QRect(0, 0, 395, 305))
        self.layout.setContentsMargins(100, 0, 100, 0)
        self.setLayout(self.layout)
        self.output_button = QPushButton(self)
        self.output_button.setText('Select Folder')
        self.layout.addWidget(self.output_button)

        self.show()
