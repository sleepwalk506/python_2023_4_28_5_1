import tkinter as tk
import pymysql
from socket import *
import time
import tkinter.messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText

import managerView as mv
import studentView as sv


try:
    db = pymysql.connect(host='localhost', user='root', passwd='', port=3306, db='python_test_db')
    print('success connect')
except:
    print('something wrong!')
cursor = db.cursor()



root1 = tk.Tk()
root1.geometry('300x150')
root1.title('LogIn')

IP = tkinter.StringVar()
IP.set('')
PORT = tkinter.StringVar()
PORT.set('')

class Select():
    def __init__(self):
        self.page0 = tk.Frame(root1)
        self.page0.pack()
        bk0 = tk.Label(self.page0, width=300, height=150)
        bk0.pack()
        managerButton = tk.Button(self.page0, text='管理�?', command=self.chooseManager)
        studentButton = tk.Button(self.page0, text='学生', command=self.chooseStudent)
        managerButton.place(x=60, y=50, width=70, height=40)
        studentButton.place(x=160, y=50, width=70, height=40)

    def chooseManager(self):
        self.page0.destroy()
        LogIn('manager')

    def chooseStudent(self):
        self.page0.destroy()
        LogIn('student')



class LogIn():

    def __init__(self,identity):
        self.identity = identity
        self.page1 = tk.Frame(root1)
        self.page1.pack()
        bk1 = tk.Label(self.page1, width=300, height=150)
        bk1.pack()

        tk.Label(self.page1)
        self.accountLabel = tk.Label(self.page1, text='账户:')
        self.accountLabel.place(x=20, y=20, width=100, height=40)
        self.accountEntry = tk.Entry(self.page1)
        self.accountEntry.place(x=120, y=20, width=100, height=30)

        self.passwordLabel = tk.Label(self.page1, text='密码:')
        self.passwordLabel.place(x=20, y=60, width=100, height=40)
        self.passwWordEntry = tk.Entry(self.page1)
        self.passwWordEntry.place(x=120, y=60, width=100, height=30)

        LogInButton = tk.Button(self.page1, text='登录',command=self.login)
        LogInButton.place(x=80, y=100, width=40, height=25)
        goBackButton = tk.Button(self.page1, text='返回', command=self.goBack)
        goBackButton.place(x=200, y=100, width=40, height=25)

    def goBack(self):
        self.page1.destroy()
        Select()

    def login(self):
        account = self.accountEntry.get()
        password = self.passwWordEntry.get()

        account = str(account)
        password = str(password)

        # values=[account,password]
        # sql = "select * from " + self.identity + " where managerName=%s and managerPassword=%s"
        # result = cursor.execute(sql, values)

        if self.identity == 'manager':
            values = [account, password]
            sql = "select * from " + self.identity + " where managerName=%s and managerPassword=%s"
        elif self.identity == 'student':
            values = [account, password]
            sql = "select * from " + self.identity + " where studentName=%s and studentPassword=%s"
        result = cursor.execute(sql,values)

        if result:
            print(f"{self.identity} login success")
            if self.identity == 'manager':
                self.page1.destroy()
                Addrlog('manager',account)
                # root1.destroy()
                # mv.ManagerView()
            elif self.identity == 'student':
                self.page1.destroy()
                Addrlog('student',account)
                # root1.destroy()
                # sv.StudentView(IP,PORT)
        else:
            print("error,please input account and password again")


class Addrlog():
    def __init__(self,identity,account):
        self.account = account
        self.identity = identity
        self.page2 = tk.Frame(root1)
        self.page2.pack()
        bk1 = tk.Label(self.page2, width=300, height=150)
        bk1.pack()

        tk.Label(self.page2)
        self.labelIP = tkinter.Label(root1, text='�?的IP地址')
        self.labelIP.place(x=20, y=5, width=100, height=40)
        self.entryIP = tkinter.Entry(root1, width=60, textvariable=IP)
        self.entryIP.place(x=120, y=10, width=100, height=30)

        self.labelPORT = tkinter.Label(root1, text='�?的�??口号')
        self.labelPORT.place(x=20, y=40, width=100, height=40)
        self.entryPORT = tkinter.Entry(root1, width=60, textvariable=PORT)
        self.entryPORT.place(x=120, y=45, width=100, height=30)

        loginButton = tkinter.Button(self.page2, text="登录", command=self.Login)
        loginButton.place(x=135, y=100, width=40, height=25)

    def Login(self):

        IP = self.entryIP.get()
        PORT = self.entryPORT.get()
        if not IP:
            tkinter.messagebox.showwarning('warning', message='�?的IP地址为空!')  # �?的IP地址为空则提�?
        elif not PORT:
            tkinter.messagebox.showwarning('warning', message='�?的�??口号为空!')  # �?的�??口号为空则提�?
        else:
            root1.destroy()
            if self.identity == 'student':
                sv.StudentView(IP, PORT,self.account)
            elif self.identity == 'manager':
                mv.ManagerView(IP,PORT,self.account)



if __name__ == '__main__':
    Select()

    root1.mainloop()
