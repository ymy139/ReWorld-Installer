from PySide6.QtGui import QFont, QFontDatabase, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QApplication
from PySide6.QtCore import Qt
from qfluentwidgets import PushButton, TextEdit, CheckBox
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
        self.resize(770, 410)
        self.setMinimumSize(770, 410)
        self.setMaximumSize(770, 410)
        self.setWindowTitle("Re-World 安装程序")
        self.setWindowIcon(QPixmap("./res/img/icon.png"))
        self.pageNum = 0
        
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 770, 410)
        self.background.setPixmap(QPixmap(".//res/img/bg.png"))
        self.background.setScaledContents(True)
        
        self.nextButton = PushButton("下一步", self)
        self.nextButton.setGeometry(630, 350, 120, 40)
        self.nextButton.setFont(QFont(self.fontInfo().family(), 14))
        self.nextButton.clicked.connect(self.nextPage)
        
        self.tipMassages = [
            QLabel(self),
            QLabel(self),
            QLabel(self)
        ]
        for index in range(3):
            self.tipMassages[index].setGeometry(10, (355+(15*index)), 360, 15)
        self.tipMassages[0].setText("程序设计: ymy139")
        self.tipMassages[1].setText("程序版本: 0.1.0   ReWorld整合包版本: 0.1.0")
        self.tipMassages[2].setText("该程序遵循[GPLv3](https://www.gnu.org/licenses/gpl-3.0-standalone.html)许可证开源，您可以在[Github](https://github.com/ymy139/ReWorld-Installer)查看源码(需要VPN)")
        self.tipMassages[2].setTextFormat(Qt.TextFormat.MarkdownText)
        self.tipMassages[2].setOpenExternalLinks(True)
        
        self.title = QLabel(self)
        self.title.setGeometry(20, 20, 400, 40)
        self.title.setFont(QFont(self.fontInfo().family(), 25))
        
        self.stepTip = QLabel(self)
        self.stepTip.setGeometry(20, 60, 355, 20)
        self.stepTip.setFont(QFont(self.fontInfo().family(), 10))
        
        self.initUI_page1()
    
    def initUI_page1(self) -> None:
        self.title.setText("欢迎使用ReWorld安装程序")
        self.stepTip.setText("该程序将引导您安装ReWorld，请确认在安装过程中网络畅通")
        self.pageNum += 1
        
    def initUI_page2(self) -> None:
        self.stepTip.setText("安装ReWorld前需要您阅读用户隐私收集及使用协议")
        self.eulaBox = TextEdit(self)
        self.eulaBox.setGeometry(20, 90, 730, 230)
        self.eulaBox.setReadOnly(True)
        self.eulaBox.setText(open("./res/docs/eula.html", "r", encoding="utf-8").read())
        self.eulaBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse     | 
                                             Qt.TextInteractionFlag.LinksAccessibleByMouse    | 
                                             Qt.TextInteractionFlag.LinksAccessibleByKeyboard |
                                             Qt.TextInteractionFlag.TextBrowserInteraction)
        self.eulaBox.show()
        self.acceptEula = CheckBox(self)
        self.acceptEula.setText("我已详细阅读并接受它们")
        self.acceptEula.setGeometry(565, 323, 185, 25)
        self.acceptEula.show()
        self.acceptEula.stateChanged.connect(self.nextButton.setEnabled)
        self.nextButton.setEnabled(False)
        self.pageNum += 1
    
    def nextPage(self) -> None:
        getattr(self, f"initUI_page{(self.pageNum+1)}")()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    exit(app.exec())