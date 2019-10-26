from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import run
import os

os.chdir("/home/joseph/Scripts/")


def load():
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    window.resize(300,400)
    label = QLabel("Print Account")
    label.setFont(QFont('SansSerif', 16))
    label.setAlignment(Qt.AlignCenter)
    
    button1 = QPushButton("\r\n6 Hours\r\n")
    button2 = QPushButton("\r\n12 Hours\r\n")
    button3 = QPushButton("\r\n1 Day\r\n")

    button1.setFont(QFont('SansSerif', 16))
    button2.setFont(QFont('SansSerif', 16))
    button3.setFont(QFont('SansSerif', 16))

    layout.addWidget(label)
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)
    window.setLayout(layout)
    button1.clicked.connect(lambda: run.print_account(6))
    button2.clicked.connect(lambda: run.print_account(12))
    button3.clicked.connect(lambda: run.print_account(24))
    window.show()
    app.exec_()

load()
