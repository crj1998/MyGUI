#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/23 20:47
#!Author: Renjie Chen
#!Function: 登录界面

from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QLabel, QPushButton, QMessageBox, QCheckBox, QGridLayout
from PyQt5.QtCore import Qt, QEvent, QRegExp, QObject, QTimer
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator, QFont, QPixmap
import random
import os

class RegisterDialog(QDialog):

    @staticmethod
    def _picpath(iconame):
        return os.path.join(os.path.dirname(os.getcwd()), 'icon', iconame)

    def __init__(self):
        super().__init__()
        self.setFixedSize(600,220)
        self.createWidgets()
        self.createGridLayout()

    def createWidgets(self):
        self.lb1 = QLabel('邮箱：',self)
        self.lb2 = QLabel('密码：', self)
        self.lb3 = QLabel('确认密码：', self)
        self.lb4 = QLabel('验证码：',self)
        self.lb1.setFixedSize(85, 20)
        self.lb2.setFixedSize(85, 20)
        self.lb3.setFixedSize(85, 20)
        self.lb4.setFixedSize(85, 20)

        self.lb1a = QLabel(self)
        self.lb2a = QLabel(self)
        self.lb3a = QLabel(self)

        self.pix_info = QPixmap(self._picpath('Info.ico'))
        self.pix_valid = QPixmap(self._picpath('Valid.ico'))
        self.pix_error = QPixmap(self._picpath('Error.ico'))
        self.lb1a.setPixmap(self.pix_info)
        self.lb2a.setPixmap(self.pix_info)
        self.lb3a.setPixmap(self.pix_info)


        self.edit1 = QLineEdit(self)
        self.edit2 = QLineEdit(self)
        self.edit3 = QLineEdit(self)
        self.edit4 = QLineEdit(self)
        self.edit1.setPlaceholderText("请注意邮箱格式")
        self.edit2.setPlaceholderText("长度不少于8位，不超过16位，必须包含数字和字母")
        self.edit3.setPlaceholderText("请再次输入密码")
        self.edit2.setContextMenuPolicy(Qt.NoContextMenu)
        self.edit3.setContextMenuPolicy(Qt.NoContextMenu)
        self.edit2.setEchoMode(QLineEdit.Password)
        self.edit3.setEchoMode(QLineEdit.Password)
        self.edit4.setEnabled(False)

        regx = QRegExp("[0-9A-Za-z]{16}$")
        validator2 = QRegExpValidator(regx, self.edit2)
        self.edit2.setValidator(validator2)
        validator3 = QRegExpValidator(regx, self.edit3)
        self.edit3.setValidator(validator3)
        regx1 = QRegExp("[0-9]{8}$")
        validator4 = QRegExpValidator(regx1, self.edit4)
        self.edit4.setValidator(validator4)

        self.bt1 = QPushButton('发送验证码',self)
        self.bt2 = QPushButton('注册', self)
        self.bt1.setEnabled(False)
        self.bt2.setEnabled(False)
        self.bt1.clicked.connect(self.sendcode)
        self.bt2.clicked.connect(self.sign_in)

        self.count = 14
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)

        self.time_100ms = QTimer(self)
        self.time_100ms.setInterval(100)
        self.time_100ms.timeout.connect(self.Refresh_100ms)
        self.time_100ms.start()


    def createGridLayout(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.lb1, 0, 1, 1, 1)
        grid.addWidget(self.lb2, 1, 1, 1, 1)
        grid.addWidget(self.lb3, 2, 1, 1, 1)
        grid.addWidget(self.lb4, 3, 1, 1, 1)
        grid.addWidget(self.edit1, 0, 2, 1, 2)
        grid.addWidget(self.edit2, 1, 2, 1, 2)
        grid.addWidget(self.edit3, 2, 2, 1, 2)
        grid.addWidget(self.edit4, 3, 2, 1, 1)
        grid.addWidget(self.lb1a, 0, 4, 1, 1)
        grid.addWidget(self.lb2a, 1, 4, 1, 1)
        grid.addWidget(self.lb3a, 2, 4, 1, 1)
        grid.addWidget(self.bt1, 3, 3)
        grid.addWidget(self.bt2, 4, 2)
        # grid.setAlignment(self.login_button,Qt.AlignCenter)

        self.setLayout(grid)

    def eventFilter(self, object, event):
        if object == self.edit2 or object == self.edit3:
            if event.type() == QEvent.MouseMove or event.type() == QEvent.MouseButtonDblClick:
                return True
            elif event.type() == QEvent.KeyPress:
                key = QKeyEvent(event)
                if key.matches(QKeySequence.SelectAll) or key.matches(QKeySequence.Copy) or key.matches(
                        QKeySequence.Paste):
                    return True
        return QDialog.eventFilter(self, object, event)

    def sign_in(self):
        if self.edit4.text() != self.code:
            self.edit4.clear()
            QMessageBox.warning(self, "警告", "验证码错误！")
        else:
            QMessageBox.information(self, "提示", "注册成功！\n账号：%s \n密码：%s"%(self.user,self.password))
            self.done(1)  # 结束对话框返回1

    def sendcode(self):
        if self.bt1.isEnabled():
            self.time_100ms.stop()
            self.edit1.setEnabled(False)
            self.edit2.setEnabled(False)
            self.edit3.setEnabled(False)
            self.code=''.join(random.sample("0123456789",8))
            print(self.code)
            self.time.start()
            self.bt1.setEnabled(False)
            self.edit4.setEnabled(True)
            self.bt1.setText('15秒后重发')
            self.user=self.edit1.text()
            self.password=self.edit2.text()
            self.bt2.setEnabled(True)


    def Refresh(self):
        if self.count > 0:
            self.bt1.setText(str(self.count)+'秒后重发')
            self.count -= 1
        else:
            self.time.stop()
            self.time_100ms.start()
            self.edit1.setEnabled(True)
            self.edit2.setEnabled(True)
            self.edit3.setEnabled(True)
            self.bt1.setEnabled(True)
            self.bt1.setText('发送验证码')
            self.count = 14

    def Refresh_100ms(self):
        text = self.edit1.text()
        if text == '':
            self.lb1a.setPixmap(self.pix_info)
            self.lb1a.setToolTip('邮箱地址为空')
            bool1 = False
        elif "@" not in text:
            self.lb1a.setPixmap(self.pix_error)
            self.lb1a.setToolTip('邮箱地址非法')
            bool1 = False
        else:
            self.lb1a.setPixmap(self.pix_valid)
            self.lb1a.setToolTip('邮箱地址合法')
            bool1 = True

        text = self.edit2.text()
        if text == '':
            self.lb2a.setPixmap(self.pix_info)
            self.lb2a.setToolTip('密码为空')
            bool2 = False
        elif 0<len(text)<8:
            self.lb2a.setPixmap(self.pix_error)
            self.lb2a.setToolTip('密码长度小于8位')
            bool2 = False
        else:
            self.lb2a.setPixmap(self.pix_valid)
            self.lb2a.setToolTip('密码有效')
            bool2 = True

        text = self.edit3.text()
        if text == '':
            self.lb3a.setPixmap(self.pix_info)
            self.lb3a.setToolTip('密码为空')
            bool3 = False
        elif text != self.edit2.text():
            self.lb3a.setPixmap(self.pix_error)
            self.lb3a.setToolTip('密码不一致')
            bool3 = False
        else:
            self.lb3a.setPixmap(self.pix_valid)
            self.lb3a.setToolTip('密码有效')
            bool3 = True

        if bool1 and bool2 and bool3:
            self.bt1.setEnabled(True)
        else:
            self.bt1.setEnabled(False)



class LoginDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setFixedSize(500,180)
        self.setWindowTitle("登录")
        self.createWidgets()
        self.createGridLayout()

        #object = QObject()

    def createWidgets(self):
        font = QFont()
        font.setItalic(True)
        #font.setBold(True)
        font.setUnderline(True)
        loginfont = QFont()
        loginfont.setPointSize(13)

        self.lb1 = QLabel('账号：',self)
        self.lb1.setFixedSize(70,30)
        self.lb1.setObjectName('lb')
        self.lb2 = QLabel("密码：", self)
        self.lb2.setFixedSize(70, 30)

        self.edit1 = QLineEdit(self)
        self.edit1.setPlaceholderText("请输入账号")
        self.edit2 = QLineEdit(self)
        self.edit2.installEventFilter(self)
        self.edit2.setContextMenuPolicy(Qt.NoContextMenu)
        self.edit2.setPlaceholderText("请输入密码")
        self.edit2.setEchoMode(QLineEdit.Password)


        self.cb1 = QCheckBox('显示密码', self)
        self.cb1.stateChanged.connect(self.check)
        self.cb2 = QCheckBox('自动登录', self)
        self.login_button = QPushButton("登  录", self)
        self.login_button.setFixedSize(300,30)
        self.login_button.setFont(loginfont)
        self.login_button.clicked.connect(self.Ok)
        self.login_button.setStyleSheet('''QPushButton{
                                                height:30px;
                                                border-style: outset;
                                                border-width: 2px;
                                                border-radius: 10px;
                                                border-color: beige;
                                                background-color: #0078d7}
                                            QPushButton:hover {
                                                background-color: #0078d7;
                                                color:white;
                                                border-style: inset;}
                                            QPushButton:pressed {
                                                background: transparent;
                                                border-style: inset;}''')

        self.bt1 = QPushButton('注册账号', self)
        self.bt1.setFixedSize(80,30)
        self.bt1.setFont(font)
        self.bt1.setStyleSheet('''QPushButton{color:black;background:transparent}
                                            QPushButton:hover {color: #0078d7}
                                            QPushButton:pressed {color: #0078d7}''')
        self.bt1.clicked.connect(self.register)
        self.bt2 = QPushButton('找回密码', self)
        self.bt2.setFixedSize(80, 30)
        self.bt2.setFont(font)
        self.bt2.setStyleSheet('''QPushButton{color:black;background:transparent}
                                                    QPushButton:hover {color: #0078d7}
                                                    QPushButton:pressed {color: #0078d7}''')


    def createGridLayout(self):
        #新建表格排列对象，并设置间距为10
        grid=QGridLayout()
        grid.setSpacing(10)
        #表格布局
        grid.addWidget(self.lb1,0,1,1,1)
        grid.addWidget(self.lb2,1,1,1,1)
        grid.addWidget(self.edit1,0,2,1,2)
        grid.addWidget(self.edit2,1,2,1,2)
        grid.addWidget(self.bt1,0,4,1,1)
        grid.addWidget(self.bt2,1,4,1,1)
        grid.addWidget(self.cb1,2,2,1,1)
        grid.addWidget(self.cb2,2,3,1,1)
        grid.addWidget(self.login_button,3,2,1,2)
        #grid.setAlignment(self.login_button,Qt.AlignCenter)

        #使能表格布局
        self.setLayout(grid)

    # 事件过滤器，防止非法输入进入密码框。
    def eventFilter(self, object, event):
        if object == self.edit2:
            if event.type() == QEvent.MouseMove or event.type() == QEvent.MouseButtonDblClick:
                return True
            elif event.type() == QEvent.KeyPress:
                key = QKeyEvent(event)
                if key.matches(QKeySequence.SelectAll) or key.matches(QKeySequence.Copy) or key.matches(
                        QKeySequence.Paste):
                    return True
        return QDialog.eventFilter(self, object, event)  # 继续传递该事件到被观察者，由其本身调用相应的事件

    def Ok(self):
        self.text = self.edit2.text()
        if len(self.text) == 0:
            QMessageBox.warning(self, "警告", "密码为空")
        elif len(self.text) < 6:
            QMessageBox.warning(self, "警告", "密码长度低于6位")
        else:
            self.done(1)  # 结束对话框返回1

    def Cancel(self):
        self.done(0)  # 结束对话框返回0

    def check(self):
        if self.sender().isChecked():
            self.edit2.setEchoMode(QLineEdit.Normal)
        else:
            self.edit2.setEchoMode(QLineEdit.PasswordEchoOnEdit)

    def register(self):
        r = RegisterDialog()
        result = r.exec_()
        if result:
            self.edit1.setText(r.user)
            self.edit2.setText(r.password)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    login = LoginDialog()
    sys.exit(login.exec_())
    #r = pwd.exec_()
    #if r:
    #    print(pwd.text)