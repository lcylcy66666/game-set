from PyQt5 import QtWidgets, QtGui, QtCore
from WorkWidget.WidgetComponents import LabelComponent
from WorkWidget.WidgetComponents import ButtonComponent

from Game.LogicMaze import LogicMaze
from Game.snake import Snake
from Game.guessNumber import GuessNumber
from Game.G2048 import G2048
from WorkWidget.rankingWidget import RankingWidget

import os

class menu(QtWidgets.QWidget):
    def __init__(self, update_widget_callback):
        super().__init__()
        self.update_widget_callback = update_widget_callback
        self.setObjectName("menu_widget")
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        # self.setStyleSheet("background-color:#2A2B6B;")
        # self.update_widget_callback = update_widget_callback
        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(35, "")
        header_label.setObjectName("header-label")
        header_label.setStyleSheet(
            """
              QLabel#header-label
              {{
                color: white;
                border-image: url(\"{}\");
              }}
            """.format("./Image/header_removeBG_1.png")
        )
        header_label.setFixedHeight(60)

        # layout = QtWidgets.QVBoxLayout()
        button_snake = ButtonComponent("貪食蛇")
        button_logic = ButtonComponent("Logic Maze")
        button_2048 = ButtonComponent("2048")
        button_guess_number = ButtonComponent("Guess Number")
        button_RANKING = ButtonComponent("Game Ranking")
        button_EXIT = ButtonComponent("Exit")

        button_snake.setFixedHeight(40)
        button_logic.setFixedHeight(40)
        button_2048.setFixedHeight(40)
        button_guess_number.setFixedHeight(40)
        button_RANKING.setFixedHeight(40)
        button_EXIT.setFixedHeight(40)

        button_snake.setObjectName("button_snake")
        button_logic.setObjectName("button_logic")
        button_2048.setObjectName("button_2048")
        button_guess_number.setObjectName("button_guess_number")
        button_RANKING.setObjectName("button_ranking")
        button_EXIT.setObjectName("button_exit")

        button_snake.setStyleSheet('QPushButton#button_snake{color: #6B5850; background-color: white; border: 2px solid #6B5850; border-radius: 5px;};')
        button_logic.setStyleSheet('QPushButton#button_logic{color:#6B5850; background-color: white; border: 2px solid #6B5850; border-radius: 5px;};')
        button_2048.setStyleSheet('QPushButton#button_2048{color: #6B5850; background-color: white; border: 2px solid #6B5850; border-radius: 5px;};')
        button_guess_number.setStyleSheet('QPushButton#button_guess_number{color: #6B5850; background-color: white; border: 2px solid #6B5850; border-radius: 5px;};')
        button_RANKING.setStyleSheet('QPushButton#button_ranking{color: #94A7AF; background-color: black; border: 2px solid #94A7AF; border-radius: 5px;};')
        button_EXIT.setStyleSheet('QPushButton#button_exit{color: #94A7AF; background-color: black; border: 2px solid #94A7AF; border-radius: 5px;};')

        button_snake.clicked.connect(self.gameWindow_snake)
        button_2048.clicked.connect(self.gameWindow_g2048)
        button_logic.clicked.connect(self.gameWindow_logic)
        button_guess_number.clicked.connect(self.gameWindow_guess)
        button_RANKING.clicked.connect(self.rankWindow)
        button_EXIT.clicked.connect(self.close_game)

        layout.addWidget(header_label, 0, 0, 1, 9)
        layout.addWidget(button_snake, 1, 0, 1, 9)
        layout.addWidget(button_logic, 2, 0, 1, 9)
        layout.addWidget(button_guess_number, 3, 0, 1, 9)
        layout.addWidget(button_2048, 4, 0, 1, 9)
        layout.addWidget(button_RANKING, 5, 0, 1, 9)
        layout.addWidget(button_EXIT, 6, 0, 1, 9)
        self.setLayout(layout)
    
    # 有秀出其他遊戲視窗的時候 不能讓主視窗被關掉的功能未實裝

    def gameWindow_snake(self):
      self.snake_window = Snake("Snake")
      self.snake_window.load()
      self.snake_window.show()

    def gameWindow_g2048(self):
      self.G2048_window = G2048("2048")
      self.G2048_window.load()
      self.G2048_window.show()
    
    def gameWindow_logic(self):
      self.logic_window = LogicMaze("LogicMaze")
      self.logic_window.load()
      self.logic_window.show()
    
    def gameWindow_guess(self):
      self.guessNumber_window = GuessNumber("Guess")
      self.guessNumber_window.load()
      self.guessNumber_window.show()
    
    def rankWindow(self):
      self.ranking_window = RankingWidget("RANKING")
      self.ranking_window.load()
      self.ranking_window.show()

    def close_game(self):
      os._exit(0)

    def load(self):
        self.setFocus()