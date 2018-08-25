#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/22 20:58
#!Author: Renjie Chen
#!Function: 主界面

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget,QLabel,QGridLayout,QListWidget,QAbstractItemView,QApplication

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.createItems()
        self.createGridLayout()
        #self.setFixedSize(500,700)
        #self.setGeometry(100,100,1400,900)
        self.setWindowTitle('main')
    def selectedItem(self):
        print(self.listwidget.currentRow())
        for i in self.listwidget.selectedItems():
            print(i.text(),end=',')
        print()
    def createItems(self):
        #导入图片并按比例缩放
        pixmap=QPixmap("0000.jpg")

        scaredPixmap=pixmap.scaled(800,800,aspectRatioMode=Qt.KeepAspectRatio)
        #放置一个标签，并显示图片
        self.lbl=QLabel(self)
        self.lbl.setFixedSize(450,750)
        self.lbl.setPixmap(pixmap)
        self.lbl.setScaledContents(True)

        l=[]
        for i in range(1,100):
            l.append(str(i))
        self.listwidget=QListWidget()
        self.listwidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.listwidget.addItems(l)
        self.listwidget.setCurrentRow(0)
        self.listwidget.itemSelectionChanged.connect(self.selectedItem)


    def createGridLayout(self):
        #界面布局，设置间距
        grid=QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.lbl,1,0)
        grid.addWidget(self.listwidget,1,1)

        self.setLayout(grid)

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=mainWindow()
    ex.show()
    sys.exit(app.exec_())