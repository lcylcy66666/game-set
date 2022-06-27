from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer

import random

# Ranking DB
from DBController.RankingInfoTable import RankingInfoTable

class LogicMaze(QtWidgets.QWidget):
    def __init__(self, update_widget):
        super().__init__()
        self.setObjectName("logic_maze")
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.update_widget_callback = update_widget
        
        layout = QtWidgets.QGridLayout()

        # 遊戲變數
        self.q_num = 1
        self.q_current_answer = 1
        self.value_timeCounter = 12
        self.value_startTime = 1000
        self.value_life = 3
        self.value_score = 0
        
        # 遊戲變數 Timer
        self.gameTimer = QTimer(self)
        self.gameTimer.timeout.connect(self.onTimer)

        # layouts

        # 遊戲畫面 遊戲外
        self.header_label = LMLabelComponent(60, "")
        self.header_label.setStyleSheet("border-image: url(./Game/LogicMaze_Image/game_title_1.png);")
        self.startBtn = NoBorderButtonComponent("Press here to START!")
        self.exitBtn = NoBorderButtonComponent("[X]", 18)
        layout.addWidget(self.header_label, 0,0,3,3)
        layout.addWidget(self.startBtn, 3,0,3,3)
        layout.addWidget(self.exitBtn, 0,3,1,1)
        self.startBtn.clicked.connect(self.startLogicMaze)
        self.exitBtn.clicked.connect(self.close_window)

        # 遊戲畫面 遊戲內
        self.question_label = LMLabelComponent(20, "")
        self.info_label_time = LMLabelComponent(16, "")
        self.info_label_data = LMLabelComponent(12, "Life: {}\nScore: {}".format(self.value_life, self.value_score))
        self.choose_1 = AnsButtonComponent("?")
        self.choose_1.clicked.connect(self.checkAnswer1)
        self.choose_2 = AnsButtonComponent("?")
        self.choose_2.clicked.connect(self.checkAnswer2)
        self.choose_3 = AnsButtonComponent("?")
        self.choose_3.clicked.connect(self.checkAnswer3)
        self.choose_1.setEnabled(False)
        self.choose_2.setEnabled(False)
        self.choose_3.setEnabled(False)
        self.message_label = LMLabelComponent(16, "")

        layout.addWidget(self.question_label,   0,0,1,3)

        layout.addWidget(self.info_label_time,  2,0,1,2)
        layout.addWidget(self.info_label_data,  2,2,1,1)

        layout.addWidget(self.choose_1,         4,0,1,1)
        layout.addWidget(self.choose_2,         4,1,1,1)
        layout.addWidget(self.choose_3,         4,2,1,1)

        layout.addWidget(self.message_label,    6,0,1,3)

        layout.setColumnStretch(0,10)
        layout.setColumnStretch(1,10)
        layout.setColumnStretch(2,10)
        layout.setColumnStretch(3,1)

        # 設定本Widget大小
        self.setFixedSize(500,300)
        self.setLayout(layout)

        #self.endLogicMaze()

    def load(self):
        self.endLogicMaze()
    
    def close_window(self):
        self.endLogicMaze()
        self.close()
    
    def return_menu(self):
        self.endLogicMaze()
        self.update_widget_callback("menu")
    
    def endLogicMaze(self):
        self.header_label.setVisible(True)
        self.startBtn.setVisible(True)

        self.question_label.setVisible(False)
        self.info_label_time.setVisible(False)
        self.info_label_data.setVisible(False)
        self.choose_1.setVisible(False)
        self.choose_2.setVisible(False)
        self.choose_3.setVisible(False)
        self.message_label.setVisible(False)

        #數字的重置
        self.q_num = 1
        # self.q_current_answer = 1
        self.value_timeCounter = 11
        self.value_startTime = 1000
        self.value_life = 3
        self.value_score = 0

        #畫面的重置
        self.question_label.clear()
        self.info_label_time.clear()
        self.info_label_data.setText("Life: {}\nScore: {}".format(self.value_life, self.value_score))
        self.choose_1.setText("?")
        self.choose_2.setText("?")
        self.choose_3.setText("?")
        self.message_label.clear()

        self.gameTimer.stop()
        #self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
    
    def startLogicMaze(self):
        self.header_label.setVisible(False)
        self.startBtn.setVisible(False)

        self.question_label.setVisible(True)
        self.info_label_time.setVisible(True)
        self.info_label_data.setVisible(True)
        self.choose_1.setVisible(True)
        self.choose_2.setVisible(True)
        self.choose_3.setVisible(True)
        self.message_label.setVisible(True)

        self.gameTimer.start(self.value_startTime)

    def onTimer(self):
        
        # 指定時間的操作
        if self.value_timeCounter == 0:
            self.answerTimeOutTime()
        elif self.value_timeCounter == 10:
            self.new_question()

        # 時間的顯示
        if self.value_timeCounter > 10:
            if self.q_num == 1:
                self.info_label_time.setText("Ready")
            else:
                if self.value_life > 0:
                    self.info_label_time.setText("Next Question...")
                else:
                    self.info_label_time.setText("")
        else:
            self.info_label_time.setText("Time Limit: {}".format(self.value_timeCounter))

        self.value_timeCounter -= 1
        
    
    def checkAnswer1(self):
        self.user_answer = int(self.choose_1.text())
        self.answerTime()
    
    def checkAnswer2(self):
        self.user_answer = int(self.choose_2.text())
        self.answerTime()
    
    def checkAnswer3(self):
        self.user_answer = int(self.choose_3.text())
        self.answerTime()
    
    def answerTime(self):
        if self.user_answer is self.q_current_answer:
            self.value_score += (10 + self.value_timeCounter)
            self.message_label.setText("Correct!! ")
        else:
            self.value_life -= 1
            self.message_label.setText("Not Correct...Ans: {}".format(self.q_current_answer))
        
        if self.value_life > 0:
            self.updateDataAndNext()
        else:
            self.gameOver()
    
    def answerTimeOutTime(self):
        self.value_life -= 1
        self.message_label.setText("Time Out...Ans: {}".format(self.q_current_answer))

        if self.value_life > 0:
            self.updateDataAndNext()
        else:
            self.gameOver()
    
    def updateDataAndNext(self):
        self.choose_1.setEnabled(False)
        self.choose_2.setEnabled(False)
        self.choose_3.setEnabled(False)

        # Life or Score Update
        self.info_label_data.setText("Life: {}\nScore: {}".format(self.value_life, self.value_score))
        
        # 重置計時器
        self.gameTimer.stop()
        self.value_timeCounter = 12
        if self.value_startTime > 100:
            self.value_startTime -= 20
        self.gameTimer.start(self.value_startTime)

    def gameOver(self):
        self.gameTimer.stop()
        ResultMessageBox("Logic Maze", "Game Over!\nYour Score: {}".format(self.value_score))
        self.rankIn(self.value_score)
        self.endLogicMaze()
    
    # 寫入 Ranking 資料庫
    def rankIn(self, score):
        if score > 0:
            name, ok = QtWidgets.QInputDialog.getText(self, "上榜囉", "請輸入您的玩家名稱")
            if ok and name:
                RankingInfoTable().insert_a_data(name, "LogicMaze", score)
        else:
            pass

    def new_question(self):

        # Q
        q_left = random.randint(0, 15)
        q_right = random.randint(0, 15)

        # random_choice?
        q_pattern = random.randint(0, 1)
        q_patternList = (
            int(q_left & q_right), 
            int(q_left | q_right), 
        )
        q_patternSymbolList = (
            "AND", 
            "OR", 
        )

        self.q_current_answer = q_patternList[q_pattern]
        self.question_label.setText("Q{}: {} {} {} = ?".format(self.q_num, q_left, q_patternSymbolList[q_pattern], q_right))
        self.q_num += 1

        # 決定答案的選項
        q_choose_ans = random.sample(range(16), 3)
        q_theCorrectOne = random.randint(0, 2)
        q_findAnsFlag = 0

        for i in range(0, len(q_choose_ans)):
            if q_choose_ans[i] == self.q_current_answer:
                q_findAnsFlag = 1
                break

        if q_findAnsFlag == 0:
            q_choose_ans[q_theCorrectOne] = self.q_current_answer

        self.message_label.setText("Please choose the right answer!")
        self.choose_1.setText(str(q_choose_ans[0]))
        self.choose_2.setText(str(q_choose_ans[1]))
        self.choose_3.setText(str(q_choose_ans[2]))

        self.choose_1.setEnabled(True)
        self.choose_2.setEnabled(True)
        self.choose_3.setEnabled(True)

        print("[LogicMaze_Debug] Q{}. 本題答案: {}".format(self.q_num -1, self.q_current_answer))

# 樣式

class ResultMessageBox(QtWidgets.QMessageBox):
    def __init__(self, MBWindowTitle, MBText):
        super().__init__()

        self.setWindowTitle(MBWindowTitle)
        self.setText(MBText)
        self.setFont(QtGui.QFont("MS Gothic", 12))

        self.exec()

class LMLabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()

        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignLeft)

        self.setFont(QtGui.QFont("MS Gothic", font_size, QtGui.QFont.Bold))
        self.setStyleSheet("border-style: none;")
        self.setText(content)

class AnsButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=18):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("MS Gothic", font_size))
        self.setStyleSheet("background-image: url(./Game/LogicMaze_Image/button_bg.png); border-style: solid; border-width: 2px; border-radius: 10px; border-color: black; min-height: 60px;")

class NoBorderButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=30):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("MS Gothic", font_size))
        self.setStyleSheet("border-style: none;")

