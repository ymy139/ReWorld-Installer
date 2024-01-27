from PySide6.QtGui import QFont, QFontDatabase, QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QApplication, QGroupBox
from PySide6.QtCore import Qt
from qfluentwidgets import PushButton, TextEdit, CheckBox, LineEdit
from psutil._common import bytes2human
import psutil
import sys
import os

REWORLD_SIZE = 630
PCL2_SIZE = 13
RESPACK_SIZE = 36
IS_DEV = True
if IS_DEV:
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "D:\项目\ReWorld-Installer\.venv\Lib\site-packages\PySide6\plugins\platforms"
else:
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = ".\PySide6\plugins\platforms"

class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.MAX_PAGE_NUM = 3
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
    
    def initUI_page3(self) -> None:
        self.eulaBox.close()
        self.acceptEula.close()
        
        self.stepTip.setText("设定安装选项")
        
        self.installItme = QGroupBox(self)
        self.installItme.setGeometry(20, 90, 730, 100)
        self.installItme.setFont(QFont(self.fontInfo().family(), 12))
        self.installItme.setTitle("安装项目")
        self.installItme.show()
        self.installItme_ReWorld = CheckBox(self.installItme)
        self.installItme_ReWorld.setGeometry(10, 20, 530, 22)
        self.installItme_ReWorld.setChecked(True)
        self.installItme_ReWorld.setText(f"ReWorld整合包 (包含Mod文件，配置文件，Minecraft可再分发文件) - {REWORLD_SIZE}MB")
        self.installItme_ReWorld.stateChanged.connect(self.recalculateSize)
        self.installItme_ReWorld.show()
        self.installItme_PCL2 = CheckBox(self.installItme)
        self.installItme_PCL2.setGeometry(10, 45, 450, 22)
        self.installItme_PCL2.setChecked(True)
        self.installItme_PCL2.setText(f"PCL2启动器 (包含启动器，启动器配置文件，教程) - {PCL2_SIZE}MB")
        self.installItme_PCL2.show()
        self.installItme_resPack = CheckBox(self.installItme)
        self.installItme_resPack.setGeometry(10, 70, 450, 22)
        self.installItme_resPack.setText(f"美化资源包 (包含提前打包好的材质，光影) - {RESPACK_SIZE}MB")
        self.installItme_resPack.show()
        
        self.installPath = QGroupBox(self)
        self.installPath.setGeometry(20, 195, 730, 75)
        self.installPath.setFont(QFont(self.fontInfo().family(), 12))
        self.installPath.setTitle("安装位置")
        self.installPath.show()
        self.installPath_display = LineEdit(self.installPath)
        self.installPath_display.setGeometry(10, 20, 640, 33)
        self.installPath_display.setPlaceholderText("默认安装在该程序所在位置")
        self.installPath_display.setReadOnly(True)
        self.installPath_display.show()
        self.installPath_find = PushButton(self.installPath)
        self.installPath_find.setGeometry(655, 20, 65, 33)
        self.installPath_find.setText("选择...")
        self.installPath_find.show()
        self.installPath_spaceTip = QLabel(self.installPath)
        self.installPath_spaceTip.setGeometry(10, 55, 710, 15)
        self.installPath_spaceTip.setFont(QFont(self.fontInfo().family(), 9))
        self.installPath_spaceTip.setText(f"需要拥有{REWORLD_SIZE + PCL2_SIZE}MB的空闲空间，当前位置有{bytes2human(psutil.disk_usage(list(os.path.abspath('.'))[0]+':').free)}B的空闲空间")
        self.installPath_spaceTip.show()
        
        self.remoteServerConfig = QGroupBox(self)
        self.remoteServerConfig.setGeometry(20, 275, 730, 60)
        self.remoteServerConfig.setFont(QFont(self.fontInfo().family(), 12))
        self.remoteServerConfig.setTitle("下载服务器配置")
        self.remoteServerConfig.show()
        self.remoteServerConfig_server_tip = QLabel(self.remoteServerConfig)
        self.remoteServerConfig_server_tip.setGeometry(10, 25, 120, 20)
        self.remoteServerConfig_server_tip.setText("下载服务器地址：")
        self.remoteServerConfig_server_tip.show()
        self.remoteServerConfig_server_input = LineEdit(self.remoteServerConfig)
        self.remoteServerConfig_server_input.setGeometry(130, 20, 300, 33)
        self.remoteServerConfig_server_input.show()
        self.remoteServerConfig_password_tip = QLabel(self.remoteServerConfig)
        self.remoteServerConfig_password_tip.setGeometry(445, 25, 70, 20)
        self.remoteServerConfig_password_tip.setText("链接密码：")
        self.remoteServerConfig_password_tip.show()
        self.remoteServerConfig_password_input = LineEdit(self.remoteServerConfig)
        self.remoteServerConfig_password_input.setGeometry(520, 20, 200, 33)
        self.remoteServerConfig_password_input.show()
        
        self.pageNum += 1
    
    def nextPage(self) -> None:
        if self.pageNum != self.MAX_PAGE_NUM and self.pageNum < self.MAX_PAGE_NUM:
            getattr(self, f"initUI_page{(self.pageNum + 1)}")()
            if self.pageNum == self.MAX_PAGE_NUM:
                self.nextButton.setText("完成")
        else:
            QApplication.exit(0)

    def recalculateSize(self) -> None:
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    exit(app.exec())