from PyQt5 import QtWidgets, QtGui, QtCore
from DBController.RankingInfoTable import RankingInfoTable

import json


class RankingWidget(QtWidgets.QWidget):
    def __init__(self, update_widget):
        super().__init__()
        self.update_widget_callback = update_widget

        self.setObjectName("ranking_widget")
        self.resize(500, 500)

        layout = QtWidgets.QGridLayout()

        header_label = rankingLabelComponent(40, "Ranking")

        self.btn_ranking_snake = rankingButtonComponent("貪食蛇")
        self.btn_ranking_logic = rankingButtonComponent("Logic Maze")
        self.btn_ranking_guessNumber = rankingButtonComponent("Guess Number")
        self.btn_ranking_2048 = rankingButtonComponent("2048")
        self.btn_ranking_snake.clicked.connect(self.show_ranking_snake)
        self.btn_ranking_logic.clicked.connect(self.show_ranking_logic)
        self.btn_ranking_guessNumber.clicked.connect(self.show_ranking_guessNumber)
        self.btn_ranking_2048.clicked.connect(self.show_ranking_2048)

        self.scroll_area_content = ScrollAreaContentWidget()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.scroll_area_content)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        layout.addWidget(header_label, 0,0,1,4)
        layout.addWidget(self.btn_ranking_snake, 1,0,1,1)
        layout.addWidget(self.btn_ranking_logic, 1,1,1,1)
        layout.addWidget(self.btn_ranking_guessNumber, 1,2,1,1)
        layout.addWidget(self.btn_ranking_2048, 1,3,1,1)

        layout.addWidget(scroll_area, 2,0,1,4)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 9)

        self.setLayout(layout)
    
    def load(self):
        self.scroll_area_content.info_label.clear()

    def show_ranking(self, game):
        info_result = RankingInfoTable().select_a_game_data(game)

        i=0
        stringOutput = ""
        for row in info_result:
            i+=1
            stringOutput += "{:>4}.  ".format(str(i))
            stringOutput += "{}    ".format(row['Date'])
            stringOutput += "{:16}".format(row['Name'])
            stringOutput += "{:16}\n".format(str(row['Score']))

        self.scroll_area_content.info_label.setText(stringOutput)
    
    def show_ranking_snake(self):
        self.show_ranking("Snake")

    def show_ranking_logic(self):
        self.show_ranking("LogicMaze")

    def show_ranking_guessNumber(self):
        self.show_ranking("GuessNumber")

    def show_ranking_2048(self):
        self.show_ranking("2048")



class ScrollAreaContentWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("show_scroll_area_widget")

        layout = QtWidgets.QVBoxLayout()

        self.info_label = rankingLabelComponent(12, "")
        layout.addWidget(self.info_label)

        self.setLayout(layout)

class rankingLabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()

        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignLeft)

        self.setFont(QtGui.QFont("Microsoft YaHei", font_size, QtGui.QFont.Bold))
        self.setText(content)

class rankingLineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", length=10, width=180, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("Microsoft YaHei", font_size))

class rankingButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=10):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("Microsoft YaHei", font_size))