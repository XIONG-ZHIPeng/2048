import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

class Game2048(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initGame()

    def initUI(self):
        self.setWindowTitle('2048')
        screen = QApplication.desktop().screenGeometry()
        x = (screen.width() - 400) // 2
        y = (screen.height() - 400) // 2
        self.setGeometry(x, y, 400, 400)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setSpacing(10)
        self.labels = [[QLabel(self) for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.labels[i][j].setFont(QFont('Arial', 24))
                self.labels[i][j].setAlignment(Qt.AlignCenter)
                self.labels[i][j].setAutoFillBackground(True)
                self.gridLayout.addWidget(self.labels[i][j], i, j)
        self.show()

    def initGame(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.addRandomTile()
        self.addRandomTile()
        self.updateUI()

    def addRandomTile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def updateUI(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                self.labels[i][j].setText(str(value) if value else '')
                palette = self.labels[i][j].palette()
                palette.setColor(QPalette.Window, QColor(255, 255, 255) if value == 0 else QColor(255, 255 - value * 5, 255 - value * 10))
                self.labels[i][j].setPalette(palette)

    def checkWin(self):
        for row in self.board:
            if 2048 in row:
                return True
        return False

    def checkGameOver(self):
        # Check for any empty tiles
        for row in self.board:
            if 0 in row:
                return False

        # Check for possible merges
        for i in range(4):
            for j in range(4):
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    return False

        return True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.moveLeft()
        elif event.key() == Qt.Key_Right:
            self.moveRight()
        elif event.key() == Qt.Key_Up:
            self.moveUp()
        elif event.key() == Qt.Key_Down:
            self.moveDown() 
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            pass

        if self.checkWin():
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("2048-You win!")
            msgBox.setText("Do you want to continue?")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msgBox.setStyleSheet("QLabel{min-width: 300px;}")
            ret = msgBox.exec_()
            if ret == QMessageBox.Yes:
                pass
            else:
                self.close()
        elif self.checkGameOver():
            msgBox = QMessageBox(self)
            msgBox.setWindowTitle("2048")
            msgBox.setText("Game over!")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Retry)
            msgBox.setStyleSheet("QLabel{min-width: 300px;}")
            ret = msgBox.exec_()
            if ret == QMessageBox.Retry:
                self.initGame()
            else:
                self.close()
        else:
            self.addRandomTile()
            self.updateUI()

    def moveLeft(self):
        for i in range(4):
            self.board[i] = self.merge(self.board[i])

    def moveRight(self):
        for i in range(4):
            self.board[i] = list(reversed(self.merge(list(reversed(self.board[i])))))

    def moveUp(self):
        self.board = self.transpose(self.board)
        self.moveLeft()
        self.board = self.transpose(self.board)

    def moveDown(self):
        self.board = self.transpose(self.board)
        self.moveRight()
        self.board = self.transpose(self.board)

    def merge(self, row):
        new_row = [i for i in row if i != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
        new_row = [i for i in new_row if i != 0]
        return new_row + [0] * (4 - len(new_row))

    def transpose(self, board):
        return [[board[j][i] for j in range(4)] for i in range(4)]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game2048()
    sys.exit(app.exec_())