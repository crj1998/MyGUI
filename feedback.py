#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/22 20:57
#!Author: Renjie Chen
#!Function: 反馈界面

from PyQt5.QtWidgets import QPushButton,QApplication,QTextEdit,QLabel,QLineEdit,QGridLayout,QComboBox,QMessageBox,QDialog
from sendEmail import sEmail


class feedbackDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.createWidgets()
        self.createGridLayout()
        self.setGeometry(300,300,450,500)
        self.setWindowTitle('用户反馈')
    def emailSubmit(self):
        if self.contactEdit.text()=='' or self.contentEdit.toPlainText()=='':
            self.warningMessage()
        elif sEmail(self.combo.currentText(),self.contactEdit.text()+'\n'+self.contentEdit.toPlainText()):
            self.successMessage()
        else:
            self.failureMessage()
    def createWidgets(self):
        self.title=QLabel('反馈类型：')
        self.contact=QLabel('邮箱地址：')
        self.content=QLabel('具体内容：')
        self.submit=QPushButton('提交')
        self.submit.clicked.connect(self.emailSubmit)
        self.combo=QComboBox()
        self.combo.addItem('意见反馈')
        self.combo.addItem('问题反馈')
        self.combo.addItem('联系作者')
        self.contactEdit=QLineEdit()
        self.contentEdit=QTextEdit()
        self.contentEdit.setText('具体描述需要反馈的内容')
        self.contentEdit.selectAll()
        self.contentEdit.setFocus(True)

    def createGridLayout(self):
        #新建表格排列对象，并设置间距为10
        grid=QGridLayout()
        grid.setSpacing(10)
        #表格布局
        grid.addWidget(self.title,1,0)
        grid.addWidget(self.combo,1,1)
        grid.addWidget(self.contact,2,0)
        grid.addWidget(self.contactEdit,2,1)
        grid.addWidget(self.content,3,0)
        grid.addWidget(self.contentEdit,3,1,5,1)
        grid.addWidget(self.submit,9,0,1,2)
        #使能表格布局
        self.setLayout(grid)
    def warningMessage(self):
        MESSAGE="<p>联系邮箱和具体内容为必填项。</p><p>点击OK返回反馈界面。</p>"
        warning=QMessageBox.information(self,'注意',MESSAGE)
    def successMessage(self):
        MESSAGE="<p>你的反馈我们已经收到，我们会尽快给您回馈，感谢您的支持。</p><p>点击OK退出反馈界面。</p>"
        success=QMessageBox.information(self,'反馈成功',MESSAGE)
        self.close()

    def failureMessage(self):
        MESSAGE="<p>由于某些原因，您没有反馈成功。<p>是否重新尝试一次？"
        failure=QMessageBox(QMessageBox.Warning,'反馈失败',MESSAGE,QMessageBox.NoButton,self)
        failure.addButton('是',QMessageBox.AcceptRole)
        failure.addButton("否",QMessageBox.RejectRole)
        if failure.exec_()==QMessageBox.AcceptRole:
            pass
        else:
            self.close()


if __name__ == '__main__':
    import sys
    app=QApplication(sys.argv)
    interface=feedbackDialog()
    interface.show()
    sys.exit(app.exec_())