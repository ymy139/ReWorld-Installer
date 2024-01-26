from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QWidget, QLabel, QApplication
import qfluentwidgets
import requests
import sys
import os

IS_DEV = True
if IS_DEV:
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "D:\项目\ReWorld-Installer\.venv\Lib\site-packages\PySide6\plugins\platforms"
else:
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = ".\PySide6\plugins\platforms"

class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        
    def initUI(self) -> None:
        self.setFont(QFont( QFontDatabase.applicationFontFamilies(
                                QFontDatabase.addApplicationFont("./res/font/Source Han Sans CN Regular.ttf"))[0],
                            9))
        
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 770, 410)
        self.background.setPixmap("/res/img/bg.jpeg")
        self.background.setScaledContents(True)
        
        self.nextButton = qfluentwidgets.PushButton("下一步", self)
        self.nextButton.setGeometry(630, 350, 120, 40)
        self.nextButton.setFont(QFont(self.fontInfo().family()), 14)
    
    def initUI_page1(self) -> None: ...
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    exit(app.exec_())