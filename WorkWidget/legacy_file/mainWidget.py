from PyQt5 import QtWidgets, QtGui, QtCore
from pip import main
from Game.LogicMaze import LogicMaze
from Game.snake import Snake
from Game.guessNumber import GuessNumber
from Game.G2048 import G2048
from WorkWidget.menuWidget import menu
from WorkWidget.rankingWidget import RankingWidget
from WorkWidget.WidgetComponents import LabelComponent, ButtonComponent


class MainWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("main_widget")
        self.setStyleSheet("background-color:#2A2B6B;")
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
        function_widget = FunctionWidget()

        layout.addWidget(header_label, 0, 0, 1, 9)
        layout.addWidget(function_widget, 1, 0, 1, 9)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 9)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 9)

        self.setLayout(layout)

class FunctionWidget(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("function_widget")
        # self.resize(300,300)
        self.widget_dict = {
            "menu": self.addWidget(menu(self.update_widget)),
            "snake": self.addWidget(Snake(self.update_widget)),
            "Logic_Maze": self.addWidget(LogicMaze(self.update_widget)),
            "Guess": self.addWidget(GuessNumber(self.update_widget)),
            "2048":self.addWidget(G2048(self.update_widget)),
            "RANKING": self.addWidget(RankingWidget(self.update_widget))
        }
        self.update_widget("menu")

        # self.setStyleSheet( "background-color:#2A2B6B;" ) 
        self.setStyleSheet("background-color: none;")
        # self.setStyleSheet("#function_widget {border-width: 2px; border-style: solid; border-color:#2A2B6B;}")

    def update_widget(self, name):
        self.setCurrentIndex(self.widget_dict[name])
        current_widget = self.currentWidget()
        current_widget.load()

    
