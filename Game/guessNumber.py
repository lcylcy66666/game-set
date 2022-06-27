from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidget.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent
from PyQt5.QtWidgets import (QLabel, QPushButton, QLineEdit)
import random
class GuessNumber(QtWidgets.QWidget):
    def __init__(self, update_widget):
        super(GuessNumber, self).__init__()
        self.update_widget_callback = update_widget
        self.num = 0  # 目標數
        self.max_num = 100  # 最大值
        self.min_num = 0  # 最小值
        self.init_ui()
    def load(self):
        self.setFocus()

    def init_ui(self):
        self.setWindowTitle('猜數字遊戲')
        self.setFixedSize(450, 290)

        # 背景顏色
        self.setStyleSheet("background: #2A2B6B;")
        self.msg = QLabel()
        self.msg.setText('猜數字遊戲(0-100)')
        self.msg.setStyleSheet(
            'font-size:50px;text-align:center;font-weight:bold;font-family:"Microsoft JhengHei";color:#E6F2F5;')
        self.msg.setAlignment(QtCore.Qt.AlignCenter)

        self.in_num = QLineEdit()
        self.in_num.setPlaceholderText('請輸入目標數字')
        self.in_num.setFixedHeight(60)
        self.in_num.setStyleSheet(
            'font-size:30px;text-align:center;font-weight:bold;font-family:"Microsoft JhengHei";color:#E6F2F5')
        self.in_num.setAlignment(QtCore.Qt.AlignCenter)

        self.in_num_btn = QPushButton()
        self.in_num_btn.setText('就是它了')
        self.in_num_btn.setFixedHeight(45)
        self.in_num_btn.clicked.connect(self.in_num_btn_click)

        self.tar_num_btn = QPushButton()
        self.tar_num_btn.setText('顯示數字')
        self.tar_num_btn.clicked.connect(self.tar_num_btn_click)

        self.tar_num = QLabel()
        self.tar_num.setText('#####')
        self.tar_num.setFixedWidth(50)

        self.generate_num_btn = QPushButton()
        self.generate_num_btn.setText('  生成目標數字  ')
        self.generate_num_btn.clicked.connect(self.generate_num_btn_click)

        self.return_menu_btn = QPushButton()
        self.return_menu_btn.setText('返回主畫面')
        self.return_menu_btn.clicked.connect(self.return_menu)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.tar_num)
        hbox.addWidget(self.tar_num_btn)
        hbox.addStretch(1)
        hbox.addWidget(self.return_menu_btn)
        hbox.addWidget(self.generate_num_btn)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.msg)
        vbox.addWidget(self.in_num)
        vbox.addWidget(self.in_num_btn)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
    
    def return_menu(self):
        self.close()
        # self.update_widget_callback("menu")

    def generate_num_btn_click(self):
        tar_num = random.randint(1, 99)
        self.num = tar_num
        # 重置最大最小值
        self.max_num = 100  # 當前最大值
        self.min_num = 0  # 當前最小值

    def tar_num_btn_click(self):
        if self.num != 0 and self.tar_num_btn.text().strip() == '顯示數字':
            self.tar_num.setText(str(self.num))
            self.tar_num_btn.setText('隱藏數字')
        elif self.tar_num_btn.text().strip() == '隱藏數字':
            self.tar_num.setText('#####')
            self.tar_num_btn.setText('顯示數字')

    def in_num_btn_click(self):
        try:
            in_num = int(self.in_num.text().strip())
            if in_num < self.min_num or in_num >= self.max_num:
                pass
            else:
                if self.num == 0:
                    self.msg.setText('沒有此數字')
                elif in_num == self.num:
                    self.msg.setText('恭喜你，猜對了')
                else:
                    if in_num < self.num:
                        self.msg.setText(str(in_num) + ' - ' + str(self.max_num))
                        self.min_num = in_num
                    elif in_num > self.num:
                        self.msg.setText(str(self.min_num) + ' - ' + str(in_num))
                        self.max_num = in_num
        except:
            self.msg.setText('請輸入數字')
