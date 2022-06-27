#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QRect
import sys
import os
import copy
import random

# Ranking DB
from DBController.RankingInfoTable import RankingInfoTable

class G2048(QMainWindow):
    def __init__(self, update_widget, parent=None):
        super(G2048, self).__init__(parent)
        self.update_widget_callback = update_widget
        self.initUi()
        # 顏色
        self.colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200),
                       8: (242, 177, 121), 16: (245, 149, 99), 32: (246, 124, 95),
                       64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 207, 114),
                       512: (237, 207, 114), 1024: (237, 207, 114), 2048: (237, 207, 114)}

        self.initGameData()

    def initUi(self):
        self.setWindowTitle("2048")
        self.resize(505, 720)

        self.setFixedSize(self.width(), self.height())
        self.initGameOpt()

    def initGameOpt(self):
        ## 遊戲初始化 
        self.lbFont = QFont('font-family', 12)  # label字體 (新細明體)
        self.lgFont = QFont('font-family', 50)  # Logo字體  (新細明體)
        self.nmFont = QFont('font-family', 36)  # 面板字體  (新細明體)

    def initGameData(self):
        ## 初始化數字 
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        count = 0
        while count < 2:
            row = random.randint(0, len(self.data) - 1)
            col = random.randint(0, len(self.data[0]) - 1)
            if self.data[row][col] != 0:
                continue
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            count += 1

        self.curScore = 0
        self.bstScore = 0
        # 载入最高得分
        if os.path.exists("2048_bestscore.txt"):
            with open("2048_bestscore.txt", "r") as f:
                self.bstScore = int(f.read())

    def paintEvent(self, e):
        # 重寫繪圖
        qp = QPainter()
        qp.begin(self)
        self.drawGameGraph(qp)
        qp.end()

    def keyPressEvent(self, e):
        keyCode = e.key()
        ret = False
        if keyCode == Qt.Key_Left:
            ret = self.move("Left")
        elif keyCode == Qt.Key_Right:
            ret = self.move("Right")
        elif keyCode == Qt.Key_Up:
            ret = self.move("Up")
        elif keyCode == Qt.Key_Down:
            ret = self.move("Down")
        else:
            pass

        if ret:
            self.repaint()  #重新渲染

    def closeEvent(self, e):
        # 保存最高得分
        with open("2048_bestscore.txt", "w") as f:
            f.write(str(self.bstScore))

    def drawGameGraph(self, qp):
        #遊戲圖形刻劃
        self.drawLog(qp)
        self.drawLabel(qp)
        self.drawScore(qp)
        self.drawBg(qp)
        self.drawTiles(qp)

    def drawScore(self, qp):
        #得分圖形刻劃
        qp.setFont(self.lbFont)
        fontsize = self.lbFont.pointSize()
        scoreLabelSize = len("SCORE") * fontsize
        bestLabelSize = len("BEST") * fontsize
        curScoreBoardMinW = 15 * 2 + scoreLabelSize  # SCORE的最小寬度
        bstScoreBoardMinW = 15 * 2 + bestLabelSize  # BEST的最小寬度
        curScoreSize = len(str(self.curScore)) * fontsize   #SCORE數字的寬度
        bstScoreSize = len(str(self.bstScore)) * fontsize   #Best數字的寬度
        curScoreBoardNedW = 10 + curScoreSize
        bstScoreBoardNedW = 10 + bstScoreSize
        curScoreBoardW = max(curScoreBoardMinW, curScoreBoardNedW)  ##最小寬度跟現有score的最大數字寬度
        bstScoreBoardW = max(bstScoreBoardMinW, bstScoreBoardNedW)  ##最小寬度與現有Best的最大數字寬度
        qp.setBrush(QColor(143, 150, 131)) ##分數背景顏色
        qp.setPen(QColor(143, 150, 131)) ##分數背景邊框顏色
        qp.drawRect(505 - 15 - bstScoreBoardW, 40, bstScoreBoardW, 50)  ##分數佔版
        qp.drawRect(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 40, curScoreBoardW, 50) ##分數佔版

        bstLabelRect = QRect(505 - 15 - bstScoreBoardW, 40, bstScoreBoardW, 25)
        bstScoreRect = QRect(505 - 15 - bstScoreBoardW, 65, bstScoreBoardW, 25)
        scoerLabelRect = QRect(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 40, curScoreBoardW, 25)
        curScoreRect = QRect(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 65, curScoreBoardW, 25)

        qp.setPen(QColor(238, 228, 218))
        qp.drawText(bstLabelRect, Qt.AlignCenter, "BEST")
        qp.drawText(scoerLabelRect, Qt.AlignCenter, "SCORE")

        qp.setPen(QColor(255, 255, 255))
        qp.drawText(bstScoreRect, Qt.AlignCenter, str(self.bstScore))
        qp.drawText(curScoreRect, Qt.AlignCenter, str(self.curScore))

    def drawBg(self, qp):
        #背景圖
        col = QColor(143, 150, 131)
        qp.setPen(col)

        qp.setBrush(QColor(143, 150, 131))
        qp.drawRect(15, 150, 475, 475)  # 遊戲區域大小

    def drawLog(self, qp):
        #2048的logo
        pen = QPen(QColor(30, 180, 30), 18) #設定顏色
        qp.setFont(self.lgFont) #基礎設定裡面的字體大小(LOGO)
        qp.setPen(pen)
        qp.drawText(QRect(10, 0, 150, 130), Qt.AlignCenter, "2048")

    def drawLabel(self, qp):
        #底下標籤訊息
        qp.setFont(self.lbFont)
        qp.setPen(QColor(119, 110, 101))
        qp.drawText(15, 134, "合併相同数字，得到2048吧!")
        qp.drawText(15, 660, "怎麼玩:")
        qp.drawText(45, 680, "用上下左右箭頭按键来移動方塊.")
        qp.drawText(45, 700, "相同數字撞上會合併在一起~~")

    def drawTiles(self, qp):
        #數字背景
        qp.setFont(self.nmFont)
        for row in range(4):
            for col in range(4):
                value = self.data[row][col]
                color = self.colors[value]

                qp.setPen(QColor(*color))
                qp.setBrush(QColor(*color))
                qp.drawRect(30 + col * 115, 165 + row * 115, 100, 100)  # 數字之間的方格
                size = self.nmFont.pointSize() * len(str(value))  # 數字長度
                # 根據尺寸調數字大小
                while size > 100 - 15 * 2:
                    self.nmFont = QFont('font-family', self.nmFont.pointSize() * 4 // 5)
                    qp.setFont(self.nmFont)
                    size = self.nmFont.pointSize() * len(str(value))  # 數字長度
                print("[%d][%d]: value[%d] weight: %d" % (row, col, value, size))

                # 非0數字顯示
                if value == 2 or value == 4:
                    qp.setPen(QColor(119, 110, 101))  # 2跟4背景比較淡 所以用深色字 
                else:
                    qp.setPen(QColor(255, 255, 255))  # 其他顏色背景比較深 所以用淺色字
                if value != 0:
                    rect = QRect(30 + col * 115, 165 + row * 115, 100, 100)
                    qp.drawText(rect, Qt.AlignCenter, str(value))

    def putTile(self):
        #找到一個空的位子（數值0），隨機塞2 OR 4
        available = []
        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                if self.data[row][col] == 0:
                    available.append((row, col))
        if available:
            row, col = available[random.randint(0, len(available) - 1)]
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            return True
        return False

    def merge(self, row):
        #合併一行或一列
        pair = False
        newRow = []
        for i in range(len(row)):
            if pair:
                newRow.append(2 * row[i])
                self.curScore += 2 * row[i]
                pair = False
            else:
                if i + 1 < len(row) and row[i] == row[i + 1]:
                    pair = True
                else:
                    newRow.append(row[i])
        return newRow

    def slideUpDown(self, isUp):
        # 上下方向移動 True上 False下
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for col in range(numCols):
            cvl = []
            for row in range(numRows):
                if self.data[row][col] != 0:
                    cvl.append(self.data[row][col])  # 將裡面的非0元素提取出来

            if len(cvl) >= 2:
                cvl = self.merge(cvl)  # 合併相同数字

            # 根據移動方向填充0
            for i in range(numRows - len(cvl)):
                if isUp:
                    cvl.append(0)
                else:
                    cvl.insert(0, 0)

            print("row=%d" % row)
            row = 0
            for row in range(numRows):
                self.data[row][col] = cvl[row]

        return oldData != self.data  # 看有沒有變化

    def slideLeftRight(self, isLeft):
        #左右移動 左true 右false
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for row in range(numRows):
            rvl = []
            for col in range(numCols):
                if self.data[row][col] != 0:
                    rvl.append(self.data[row][col])

            if len(rvl) >= 2:
                rvl = self.merge(rvl)

            for i in range(numCols - len(rvl)):
                if isLeft:
                    rvl.append(0)
                else:
                    rvl.insert(0, 0)

            col = 0
            for col in range(numCols):
                self.data[row][col] = rvl[col]

        return oldData != self.data

    def move(self, direction):
        # 移動
        isMove = False
        if direction == "Up":
            isMove = self.slideUpDown(True)
        elif direction == "Down":
            isMove = self.slideUpDown(False)
        elif direction == "Left":
            isMove = self.slideLeftRight(True)
        elif direction == "Right":
            isMove = self.slideLeftRight(False)
        else:
            pass

        if not isMove:
            return False

        self.putTile()  # 新增一个數字
        if self.curScore > self.bstScore:
            self.bstScore = self.curScore
            self.closeEvent(0)

        if self.isGameOver():

            # gameover 寫入排行榜
            self.rankIn(self.curScore)

            # 改成按掉msgbox就重來
            QMessageBox.warning(self, "Warning", u"GGs，restart？", QMessageBox.Ok, QMessageBox.Ok)

            self.initGameOpt()
            bstScore = self.bstScore
            self.initGameData()
            self.bstScore = bstScore
            return True

        else:
            return True

    def isGameOver(self):
        # 判斷遊戲能否繼續
        copyData = copy.deepcopy(self.data)  # 暫存數據
        curScore = self.curScore

        flag = False
        if not self.slideUpDown(True) and not self.slideUpDown(False) and \
                not self.slideLeftRight(True) and not self.slideLeftRight(False):
            flag = True  # 全部方向都不能再移動
        self.curScore = curScore
        if not flag:
            self.data = copyData  # 仍可以動，則恢復原本的數據
        return flag

    # 寫入 Ranking 資料庫
    def rankIn(self, score):
        if score > 0:
            name, ok = QInputDialog.getText(self, "上榜囉", "請輸入您的玩家名稱")
            if ok and name:
                RankingInfoTable().insert_a_data(name, "2048", score)
        else:
            pass

    def load(self):
        # self.setFocus()
        print("[G2048 Debug] LOAD")
        self.initGameData()

    def return_menu(self):
        self.update_widget_callback("menu")

#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    form = G2048()
#    form.show()
#    sys.exit(app.exec_())

'''https://www.geeksforgeeks.org/2048-game-in-python/'''
'''https://chowdera.com/2022/02/202202200338353411.html'''