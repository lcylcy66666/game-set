from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QInputDialog
from PyQt5.QtGui import QPainter, QPen, QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QBasicTimer
import sys
import random
import os
from collections import deque

# Ranking DB
from DBController.RankingInfoTable import RankingInfoTable

class Snake(QWidget):

    def __init__(self, update_widget):
        super().__init__()
        self.update_widget_callback = update_widget
        palette1 = QPalette()  # 背景設為黑
        palette1.setColor(self.backgroundRole(), QColor(0, 0, 0))
        self.setPalette(palette1)

    def load(self):
        #self.setFocus()
        self.init()  
    
    def init(self):

        self.moveWay = 1 # 判斷移動方向的flag(0123: 上右下左) 蛇不可以往自身移動方向的反方向移動
        
        self.message_box_run()  # 跳出message選擇難度，決定速度
        self.init_ui()  # 初始化ui
        self.draw_init()  # 圖形初始化
        
    def return_menu(self):
        self.update_widget_callback("menu")

    def init_ui(self):

        #視窗大小

        self.setFixedSize(self.width(), self.height())
        self.setFixedSize(400, 300)

        self.timer = QBasicTimer()  # 開啟時鐘
        self.timer.start(self.global_speed, self)  #步數是messagebox傳來的難度決定速度

    def message_box_run(self):
        print("messsage_box_run: START!")
        int_, ok = QInputDialog().getInt(QWidget(), '遊戲難度', '難度1-10:', 8, 1, 10)
        self.global_speed = (-int_ + 11)*100
        self.global_diff = int_

    def timerEvent(self, a0) -> None:
        self.update()  # 透過時間訊號更新圖像

    def paintEvent(self, e):
        self.qp = QPainter()  # 畫面工具繼承
        self.qp.begin(self)  # 開啟
        self.drawPoints(self.qp)
        self.qp.end()

    def change_food(self):  # 食物生成
        size = self.size()
        self.point_food = [random.randint(2, size.width() // 10 - 2) * 10,
                           random.randint(2, size.height() // 10 - 2) * 10]

    def drawPoints(self, qp):
        speed = 10  # 每一步為10pixel
        point_temp = self.point

        # 改變蛇的顏色
        qp.setPen(QPen(Qt.yellow, 10))  # 設定畫筆
        qp.drawPoint(self.point_food[0], self.point_food[1])  # 顯示食物

        if point_temp[-1] == self.point_food:  # 對吃下去的食物處理
            self.point_temp_food.append(self.point_food)
            self.change_food()  # 被吃後更新食物位置
            while self.point_food in self.point:  # 避免食物出現在蛇的身上，直到不出現在蛇身上
                self.change_food()

        # 移動軌跡，尾部減一，頭+1

        if self.key_word == Qt.Key_Right and self.moveWay != 3:
            point_temp.popleft()  # 左邊尾巴
            point_temp.append([(point_temp[-1][0] + speed), (point_temp[-1][1])])
            if point_temp[0] in self.point_temp_food:  # 如果發現頭部和食物重疊就夾在尾巴
                self.point_temp_food.remove(point_temp[0])
                point_temp.append(point_temp[-1])
            self.moveWay = 1

        elif self.key_word == Qt.Key_Left and self.moveWay != 1:
            point_temp.popleft()
            point_temp.append([(point_temp[-1][0] - speed), (point_temp[-1][1])])
            if point_temp[0] in self.point_temp_food:
                self.point_temp_food.remove(point_temp[0])
                point_temp.append(point_temp[-1])
            self.moveWay = 3

        elif self.key_word == Qt.Key_Down and self.moveWay != 0:
            point_temp.popleft()
            point_temp.append([(point_temp[-1][0]), (point_temp[-1][1]) + speed])
            if point_temp[0] in self.point_temp_food:
                self.point_temp_food.remove(point_temp[0])
                point_temp.append(point_temp[-1])
            self.moveWay = 2

        elif self.key_word == Qt.Key_Up and self.moveWay != 2:
            point_temp.popleft()
            point_temp.append([(point_temp[-1][0]), (point_temp[-1][1]) - speed])
            if point_temp[0] in self.point_temp_food:
                self.point_temp_food.remove(point_temp[0])
                point_temp.append(point_temp[-1])
            self.moveWay = 0

        for x, y in point_temp:  # 畫出蛇和食物
            qp.drawPoint(x, y)

        self.point = point_temp  # 更新蛇的樣子
        self.dead_()  # 判斷是否死亡
    def keyPressEvent(self, event):  # 按鍵控制
        if event.key() == Qt.Key_Right and self.key_word == Qt.Key_Left:  # 向左不能向右
            return
        elif event.key() == Qt.Key_Left and self.key_word == Qt.Key_Right:
            return
        elif event.key() == Qt.Key_Down and self.key_word == Qt.Key_Up:  # 向上就不能向下
            return
        elif event.key() == Qt.Key_Up and self.key_word == Qt.Key_Down:
            return
        elif event.key() == Qt.Key_Escape:  # esc退出
            self.close()

        self.key_word = event.key()  # 儲存信號

    def draw_init(self):
        self.point = deque([[130, 150], [140, 150], [150, 150], [160, 150], [170, 150]])  # 初始長度
        self.point_food = [240, 150]  # 初始食物
        self.point_temp_food = deque([])  # 吃下去的食物
        self.key_word = Qt.Key_Right  # 案件數據
        self.qp_init = QPainter()  # 初始化繪圖
        self.qp_init.begin(self)
        self.qp_init.setPen(QPen(Qt.yellow, 10))
        for x, y in self.point:
            self.qp_init.drawPoint(x, y)
        self.qp_init.end()

    def dead_(self):
        size = self.size()
        point_temp = self.point.copy()  # 淺複製
        for s in self.point_temp_food:  # 移除干擾的食物
            if s in point_temp:
                point_temp.remove(s)
        point_temp.pop()  # 移除頭部
        point_temp.pop()
        if self.point[-1] in point_temp:  # 頭和身體重疊就死了
            self.dead_decide()
        elif self.point[-1][0] == size.width()-0 or self.point[-1][1] == size.height()-0 \
                or self.point[-1][0] == 0 or self.point[-1][1] == 0:  # 頭部碰到四個邊界
            self.dead_decide()
    def dead_decide(self):

        Total_Score = int(len(self.point)-5) * (self.global_diff/1)

        Mbox = QMessageBox()
        Mbox.information(self, 'Snake', "難度{}遊戲結束，得分為{}".format(self.global_diff, Total_Score)) # 跳出meessagebox顯示分數

        #Ranking
        self.rankIn(Total_Score)

        Mbox_Exit = QMessageBox().question(self, 'Snake', "要繼續遊戲嗎？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if Mbox_Exit == QMessageBox.Yes:
            self.init()
        else:
            self.close()  # 關閉

    # 寫入 Ranking 資料庫
    def rankIn(self, score):
        if score > 0:
            name, ok = QInputDialog.getText(self, "上榜囉", "請輸入您的玩家名稱")
            if ok and name:
                RankingInfoTable().insert_a_data(name, "Snake", score)
        else:
            pass

'''https://pythontechworld.com/article/detail/tEUhfRryJKKM'''