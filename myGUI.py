#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/22 20:59
#!Author: Renjie Chen
#!Function: 基础界面框架

import sys
import os
from binascii import hexlify
from PyQt5.QtCore import Qt,QSettings
from os.path import join as opj
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QAction, qApp, QInputDialog, QFileDialog, QMenu, QActionGroup

from feedback import feedbackDialog
from aboutme import aboutDialog

def viptest(p):
    if len(p)!=20:return False
    pubKey='010001'
    modulus='00e0b509f6259df8'
    text=p[:5]
    text=text[::-1].encode()
    rsa=int(hexlify(text),16)**int(pubKey,16)%int(modulus,16)
    return format(rsa,'x').zfill(15)==p[5:]


class rootWindow(QMainWindow):
    #windowList=[]
    @staticmethod
    def openico(iconame):
        return opj(os.path.dirname(os.getcwd()),'icon',iconame)

    def __init__(self):
        super().__init__()
        self.createSettings()
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.setGeometry(100,100,1300,900)
        self.setWindowTitle('APP')
        self.setWindowIcon(QIcon(self.openico('download.ico')))
        #self.setCentralWidget(mainWindow())
        self.show()

    def createSettings(self):
        self.setting=QSettings('MySoft','Beautyleg Downloader')

    def createActions(self):
        self.openAct=QAction(QIcon(self.openico('open.ico')),'打开...',self,shortcut="Ctrl+O",triggered=self.openfile,statusTip='打开文件')
        self.printAct=QAction("打印",self,shortcut="Ctrl+P",enabled=False,triggered=self.print_)    #初始状态不可点击
        self.exitAct=QAction("退出",self,shortcut="Ctrl+Q",triggered=self.close)
        self.debug=QAction('开发者模式',self,statusTip='本功能为开发者调试功能，用户请勿使用！',checkable=True,enabled=False)
        self.user=QAction('用户模式',self,statusTip='目前为用户模式！',checkable=True)
        self.activation=QAction(QIcon(self.openico('vip.ico')),'激活VIP',self,shortcut="Ctrl+V",triggered=self.showDialog_VIP,statusTip='激活VIP功能')
        self.aboutappAct = QAction("关于应用",self,triggered=self.aboutapp)
        self.aboutmeAct = QAction("关于作者", self, triggered=self.aboutme)
        self.aboutQtAct = QAction("关于Qt", self, triggered=QApplication.instance().aboutQt)
        self.feedbackAct = QAction(QIcon(self.openico('feedback.ico')), '反馈', self, triggered=self.feedback)
        self.yearall = QAction('全部',self, statusTip='全部年份的套图', checkable=True, triggered=self.allyear)
        self.year2018 = QAction('2018',self,statusTip='2018年份的套图', checkable=True, triggered=self.oneyear)
        self.year2017 = QAction('2017', self, statusTip='2017年份的套图', checkable=True, triggered=self.oneyear)
        self.year2016 = QAction('2016', self, statusTip='2016年份的套图', checkable=True, triggered=self.oneyear)
        self.year2015 = QAction('2015', self, statusTip='2015年份的套图', checkable=True, triggered=self.oneyear)

        self.alignmentGroup = QActionGroup(self)
        self.alignmentGroup.addAction(self.user)
        self.alignmentGroup.addAction(self.debug)
        self.user.setChecked(True)

        if self.setting.value('isVip',0)==1:
            self.activation.setEnabled(False)
            self.activation.setStatusTip('VIP已激活')


    def createMenus(self):
        yearmenu = QMenu('年份',self)
        yearmenu.addAction(self.yearall)
        yearmenu.addSeparator()
        yearmenu.addAction(self.year2018)
        yearmenu.addAction(self.year2017)
        yearmenu.addAction(self.year2016)
        yearmenu.addAction(self.year2015)

        modemenu = QMenu('模式切换',self)
        modemenu.addAction(self.user)
        modemenu.addAction((self.debug))

        fileMenu=self.menuBar().addMenu("文件(&F)")
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.printAct)
        fileMenu.addSeparator()    #添加一条横线
        fileMenu.addAction(self.exitAct)

        settingMenu = self.menuBar().addMenu('设置(&S)')
        settingMenu.addMenu(yearmenu)
        settingMenu.addSeparator()
        settingMenu.addMenu(modemenu)

        feedbackMenu = self.menuBar().addMenu('反馈(&B)')
        feedbackMenu.addAction(self.feedbackAct)

        aboutMenu=self.menuBar().addMenu("关于(&A)")
        aboutMenu.addAction(self.aboutappAct)
        aboutMenu.addAction(self.aboutmeAct)
        aboutMenu.addAction(self.aboutQtAct)

        #重新进行菜单排序
        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(settingMenu)
        self.menuBar().addMenu(feedbackMenu)
        self.menuBar().addMenu(aboutMenu)

    def createToolBars(self):
        self.toolbar=self.addToolBar('Activate')
        self.toolbar.addAction(self.activation)

    def createStatusBar(self,words='待命中'):
        self.statusBar().showMessage(words)

    def openfile(self):
        fname=QFileDialog.getOpenFileName(self,'Open file',os.getcwd())

    def print_(self):
        dialog=QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter=QPrinter(self.printer)
            rect=painter.viewport()
            size=self.imageLabel.pixmap().size()
            size.scale(rect.size(),Qt.KeepAspectRatio)
            painter.setViewport(rect.x(),rect.y(),size.width(),size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0,0,self.imageLabel.pixmap())

    def showDialog_VIP(self):
        text,ok=QInputDialog.getText(self,'激活VIP','输入激活码:')
        if ok:
            if viptest(text):
                self.setting.setValue('isVip',1)
                self.activation.setEnabled(False)
                self.activation.setStatusTip('VIP已激活')
                self.createStatusBar("激活成功")
            else:
                self.createStatusBar("激活失败")

    def aboutapp(self):
        QMessageBox.about(self, "About Beautyleg Downloader","<p>应用 <b>Beautyleg Downloader</b> 可以用于下载Beautyleg套图，支持在线预览，图包下载，VIP用户可以多图包下载。</p>" 
                          "<p>本应用仅作为交流学习使用，请勿用于商业用途，否则后果自负。</p>" 
                          "<p>本应用中的所有图片版权归Beautyleg所有。</p>")
    def aboutme(self):
        abm=aboutDialog()
        r=abm.exec_()


    def feedback(self):
        fbd=feedbackDialog()
        r=fbd.exec_()
        #fbd.setWindowIcon(QIcon(self.openico('feedback.ico')))
        #self.windowList.append(fbd)
        #fb.show()

    def allyear(self):
        if self.yearall.isChecked():
            self.year2018.setChecked(True)
            self.year2017.setChecked(True)
            self.year2016.setChecked(True)
            self.year2015.setChecked(True)
        else:
            self.year2018.setChecked(False)
            self.year2017.setChecked(False)
            self.year2016.setChecked(False)
            self.year2015.setChecked(False)

    def oneyear(self):
        if self.year2018.isChecked() and self.year2017.isChecked() and self.year2016.isChecked() and self.year2015.isChecked():
            self.yearall.setChecked(True)
        else:
            self.yearall.setChecked(False)



    #右键菜单
    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        refreshAct = cmenu.addAction("刷新")
        quitAct = cmenu.addAction("退出")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAct:
            qApp.quit()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=rootWindow()
    ex.show()
    sys.exit(app.exec_())




