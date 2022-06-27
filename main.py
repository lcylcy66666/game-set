from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QPushButton, QWidget, QHBoxLayout, QToolBar, QVBoxLayout, QMessageBox,QShortcut

from WorkWidget.WidgetComponents import LabelComponent
from WorkWidget.menuWidget import menu

from PyQt5.QtGui import QIcon,QKeySequence
from PyQt5 import sip
import sys

# SQLite3
from DBController.DBConnection import DBConnection
from DBController.DBInitializer import DBInitializer
from DBController.RankingInfoTable import RankingInfoTable


class Main(QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        
        self.setWindowTitle('Game')
        self.setFixedSize(530, 530) #530 780

        #Set Icon
        self.setWindowIcon(QIcon('Image/game-console.png'))

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        # '''shortcut control'''
        # self.msgSc = QShortcut(QKeySequence('Ctrl+W'), self)
        # self.msgSc.activated.connect(self.back_to_menu)
       
        # ''' set toobar'''
        # toolbar = QToolBar("Toolbar")
        # toolbar.setObjectName("tool_bar")
        # toolbar.setFixedHeight(40)

        # '''ToolBar'''
        # self.addToolBar(toolbar)
        # button_quit = QAction(QIcon('./Image/logout.png') ,"Back to menu", self)
        # self.setStyleSheet("QToolBar {background: #2A2B6B;}")
        # button_quit.triggered.connect(self.back_to_menu)
        # toolbar.addAction(button_quit)

        '''Layout'''
        self.functiona_widget = menu("menu")
        layout = QVBoxLayout()
        layout.addWidget(self.functiona_widget)

        '''Create widget'''
        main_frame = QWidget()
        main_frame.setLayout(layout)
        #視窗居中
        self.setCentralWidget(main_frame)

        '''SQLite3'''
        DBConnection.db_file_path = "game_ranking.db"
        DBInitializer().execute()

    # def back_to_menu(self):
    #     reply = QMessageBox.question(self, 'Message', f"確認是否返回畫面", QMessageBox.No |
    #                                         QMessageBox.Yes, QMessageBox.Yes)  # 跳出meessagebox顯示分數
    #     if reply == QMessageBox.No: 
    #         pass
    #     else:
    #         self.functiona_widget.update_widget("menu")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Main()

    # 背景的顏色
    win.setStyleSheet("QMainWindow {color: yellow;}")
    
    win.show()
    sys.exit(app.exec_())
