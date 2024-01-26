from PySide6 import QtCore, QtGui, QtWidgets
from qfluentwidgets import PushButton
import requests

class Window(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        