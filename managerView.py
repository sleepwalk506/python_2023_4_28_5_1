import tkinter as tk
import pymysql
from socket import *
import time
import tkinter.messagebox
import threading
import json
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
import tkinter.font as tf

root2 = tk.Tk()
root2.geometry('640x480')
root2.title('Manager')

IP = '127.0.0.1'
SERVER_PORT = 50000
user = ''
listbox1 = ''  # 用于显示在线用户的列表�??
show = 1  # 用于判断�?开还是关闭列表�?
users = []  # 在线用户列表
chat = '0'  # 聊天对象
chat_pri = ''

# ft = tf.Font(font=("华文行楷",40,tf.BOLD))

try:
    db = pymysql.connect(host='localhost', user='root', passwd='', port=3306, db='python_test_db')
    print('success connect')
except:
    print('something wrong!')
cursor = db.cursor()

class ManagerView():
    def __init__(self,MAIP,MAPORT,account):
        self.user = account
        self.STUIP = MAIP
        self.STUPORT = MAPORT
        self.msglist = []
        print(MAIP, MAPORT)
        self.createPage()

    def createPage(self):
        self.show_all_frame = tk.Frame(root2)
        self.insertIn_frame = tk.Frame(root2)
        self.query_bar_frame = tk.Frame(root2)
        self.delete_bar_frame = tk.Frame(root2)
        self.update_bar_frame = tk.Frame(root2)
        self.chat_frame = tk.Frame(root2)

        self.ip_port = (self.STUIP, int(self.STUPORT))
        self.s = socket(AF_INET, SOCK_DGRAM)
        if self.user:
            self.s.sendto(self.user.encode(), self.ip_port)  # 发送用户名
        else:  # �?删除，因为已经确保用户名不为空了
            self.s.sendto('用户名不存在', self.ip_port)
            self.user = self.STUIP + ':' + self.STUPORT

        r = threading.Thread(target=self.receive)
        r.start()  # 开始线程接收信�?

        menubar = tk.Menu(root2)
        menubar.add_command(label='全部',command=self.show_all)
        menubar.add_command(label='录入',command=self.insertIn)
        menubar.add_command(label='查�??',command=self.query_bar)
        menubar.add_command(label='删除',command=self.delete_bar)
        menubar.add_command(label='�?�?',command=self.update_bar)
        menubar.add_command(label='交流',command=self.chat_bar)
        root2['menu'] = menubar

        root2.mainloop()

    def show_all(self):
        self.chat_frame.pack_forget()
        self.show_all_frame = tk.Frame(root2)
        self.insertIn_frame.destroy()
        self.query_bar_frame.destroy()
        self.delete_bar_frame.destroy()
        self.update_bar_frame.destroy()
        # self.show_all_frame = tk.Frame(root2)
        self.show_all_frame.pack()
        self.show_all_frame.place(x=0, y=30, width=640, height=440)
        listbox = ScrolledText(self.show_all_frame)
        listbox.place(x=5, y=10, width=620, height=400)

        sql = "select * from lessons"
        result = cursor.execute(sql)
        info = cursor.fetchall()#tuple
        infoList = list(info)
        # print(type(infoList))
        # print(info)
        # print(type(info))
        for i in range(result):
            for j in infoList[i]:
                k = str(j)
                listbox.insert(tkinter.END,k.ljust(10))#'{0:<15}'.format(j)
            listbox.insert(tkinter.END, '\n')
            listbox.insert(tkinter.END,'------------------------------------------------------------------------------------')
            listbox.insert(tkinter.END, '\n')

    def insertIn(self):
        self.chat_frame.pack_forget()
        self.insertIn_frame = tk.Frame(root2)
        self.show_all_frame.destroy()
        self.query_bar_frame.destroy()
        self.delete_bar_frame.destroy()
        self.update_bar_frame.destroy()
        self.insertIn_frame.pack()

        self.front_add = "insert into lessons(lessonName,lessonNumber,teacherName,lessonHour,credit,courseProperties) "
        # self.insertIn_frame = tk.Frame(root2)

        self.insertIn_frame.place(x=0, y=30, width=640, height=440)
        self.insert_entry = tk.Entry(self.insertIn_frame)
        self.insert_entry.place(x=100,y=150,width=440,height=250)

        insertButton = tk.Button(self.insertIn_frame,text='插入',command=self.get_command)
        insertButton.place(x=300, y=100, width=40, height=25)

    def get_command(self):
        self.insert_command = self.insert_entry.get()
        sql = self.front_add + 'values(' + self.insert_command + ')'
        result = cursor.execute(sql)
        db.commit()
        if result:
            print("insert success")
        else:
            print("error")

    def query_bar(self):
        self.chat_frame.pack_forget()
        self.query_bar_frame = tk.Frame(root2)
        self.show_all_frame.destroy()
        self.insertIn_frame.destroy()
        self.delete_bar_frame.destroy()
        self.update_bar_frame.destroy()
        self.query_bar_frame.pack()
        self.query_bar_frame.place(x=0, y=30, width=640, height=440)

        tk.Label(self.query_bar_frame,text='按�?�程编号').place(x=100,y=20,width=100,height=40)
        self.number_entry = tk.Entry(self.query_bar_frame)
        self.number_entry.place(x=200,y=25,width=120,height=30)
        select_by_number_button = tk.Button(self.query_bar_frame,text='查�??',command=self.query_by_number)
        select_by_number_button.place(x=320,y=25,width=40,height=30)

        tk.Label(self.query_bar_frame, text='按�?�程名称').place(x=100, y=60, width=100, height=40)
        self.name_entry = tk.Entry(self.query_bar_frame)
        self.name_entry.place(x=200, y=65, width=120, height=30)
        select_by_name_button = tk.Button(self.query_bar_frame, text='查�??',command=self.query_by_name)
        select_by_name_button.place(x=320, y=65, width=40, height=30)

        self.listbox_query = ScrolledText(self.query_bar_frame)
        self.listbox_query.place(x=5, y=100, width=620, height=300)

    def query_by_number(self):
        self.listbox_query.delete(1.0,'end')

        self.query_by_number_command = self.number_entry.get()
        sql = "select * from lessons where lessonNumber=" + self.query_by_number_command
        result = cursor.execute(sql)
        info = cursor.fetchall()
        infoList = list(info)

        for i in range(result):
            for j in infoList[i]:
                k = str(j)
                self.listbox_query.insert(tkinter.END, k.ljust(10))  # '{0:<15}'.format(j)
            self.listbox_query.insert(tkinter.END, '\n')
            self.listbox_query.insert(tkinter.END,
                           '------------------------------------------------------------------------------------')
            self.listbox_query.insert(tkinter.END, '\n')
    def query_by_name(self):
        self.listbox_query.delete(1.0,'end')

        self.query_by_name_command = self.name_entry.get()
        value = [self.query_by_name_command]
        sql = "select * from lessons where lessonName=%s"
        result = cursor.execute(sql,value)
        info = cursor.fetchall()
        infoList = list(info)

        for i in range(result):
            for j in infoList[i]:
                k = str(j)
                self.listbox_query.insert(tkinter.END, k.ljust(10))  # '{0:<15}'.format(j)
            self.listbox_query.insert(tkinter.END, '\n')
            self.listbox_query.insert(tkinter.END,
                           '------------------------------------------------------------------------------------')
            self.listbox_query.insert(tkinter.END, '\n')

    def delete_bar(self):
        self.chat_frame.pack_forget()
        self.delete_bar_frame = tk.Frame(root2)
        self.insertIn_frame.destroy()
        self.show_all_frame.destroy()
        self.query_bar_frame.destroy()
        self.update_bar_frame.destroy()
        self.delete_bar_frame.pack()
        self.delete_bar_frame.place(x=0, y=30, width=640, height=440)

        tk.Label(self.delete_bar_frame, text='按�?�程编号').place(x=100, y=20, width=100, height=40)
        self.delete_number_entry = tk.Entry(self.delete_bar_frame)
        self.delete_number_entry.place(x=200, y=25, width=120, height=30)
        delete_by_number_button = tk.Button(self.delete_bar_frame, text='删除', command=self.delete_by_number)
        delete_by_number_button.place(x=320, y=25, width=40, height=30)

        tk.Label(self.delete_bar_frame, text='按�?�程名称').place(x=100, y=60, width=100, height=40)
        self.delete_name_entry = tk.Entry(self.delete_bar_frame)
        self.delete_name_entry.place(x=200, y=65, width=120, height=30)
        delete_by_name_button = tk.Button(self.delete_bar_frame, text='删除', command=self.delete_by_name)
        delete_by_name_button.place(x=320, y=65, width=40, height=30)

        self.listbox_delete = ScrolledText(self.delete_bar_frame)
        self.listbox_delete.place(x=5, y=100, width=620, height=300)

    def delete_by_number(self):
        self.listbox_delete.delete(1.0, 'end')

        self.delete_by_number_command = self.delete_number_entry.get()
        value = [self.delete_by_number_command]
        sql = "delete from lessons where lessonNumber=%s"
        cursor.execute(sql,value)
        db.commit()

        sql = "select * from lessons"
        result = cursor.execute(sql)
        info = cursor.fetchall()
        infoList = list(info)

        for i in range(result):
            for j in infoList[i]:
                k = str(j)
                self.listbox_delete.insert(tkinter.END, k.ljust(10))  # '{0:<15}'.format(j)
            self.listbox_delete.insert(tkinter.END, '\n')
            self.listbox_delete.insert(tkinter.END,
                                      '------------------------------------------------------------------------------------')
            self.listbox_delete.insert(tkinter.END, '\n')
    def delete_by_name(self):
        self.listbox_delete.delete(1.0, 'end')

        self.delete_by_name_command = self.delete_name_entry.get()
        value = [self.delete_by_name_command]
        sql = "delete from lessons where lessonName=%s"
        cursor.execute(sql, value)
        db.commit()

        sql = "select * from lessons"
        result = cursor.execute(sql)
        info = cursor.fetchall()
        infoList = list(info)

        for i in range(result):
            for j in infoList[i]:
                k = str(j)
                self.listbox_delete.insert(tkinter.END, k.ljust(10))  # '{0:<15}'.format(j)
            self.listbox_delete.insert(tkinter.END, '\n')
            self.listbox_delete.insert(tkinter.END,
                                       '------------------------------------------------------------------------------------')
            self.listbox_delete.insert(tkinter.END, '\n')

    def update_bar(self):
        self.chat_frame.pack_forget()
        self.delete_bar_frame.destroy()
        self.insertIn_frame.destroy()
        self.show_all_frame.destroy()
        self.query_bar_frame.destroy()
        self.update_bar_frame = tk.Frame(root2)
        self.update_bar_frame.pack()
        self.update_bar_frame.place(x=0, y=30, width=640, height=440)

        self.update_entry = tk.Entry(self.update_bar_frame)
        self.update_entry.place(x=100, y=90, width=440, height=100)
        update_button = tk.Button(self.update_bar_frame, text='更新',command=self.update_command)
        update_button.place(x=300, y=50, width=40, height=25)

        self.listbox_update = ScrolledText(self.update_bar_frame)
        self.listbox_update.place(x=5,y=200,width=620,height=200)
    def update_command(self):
        update_com = self.update_entry.get()
        sql = update_com
        cursor.execute(sql)
        db.commit()

        sql = "select * from lessons"
        result = cursor.execute(sql)
        info = cursor.fetchall()
        infoList = list(info)

        for i in range(result):
            for j in infoList[i]:
                k = str(j)
                self.listbox_update.insert(tkinter.END, k.ljust(10))  # '{0:<15}'.format(j)
            self.listbox_update.insert(tkinter.END, '\n')
            self.listbox_update.insert(tkinter.END,
                                       '------------------------------------------------------------------------------------')
            self.listbox_update.insert(tkinter.END, '\n')

    def chat_bar(self):
        self.delete_bar_frame.destroy()
        self.insertIn_frame.destroy()
        self.show_all_frame.destroy()
        self.query_bar_frame.destroy()
        self.update_bar_frame.destroy()

        self.chat_frame = tk.Frame(root2)
        self.chat_frame.pack()
        self.chat_frame.place(x=0, y=20, width=640, height=440)

        self.chatbox = ScrolledText(self.chat_frame)
        self.chatbox.place(x=5, y=10, width=620, height=350)

        self.chat_entry = tk.Entry(self.chat_frame)
        self.chat_entry.place(x=5, y=370, width=500, height=80)

        send_button = tk.Button(self.chat_frame,text='发�?',command=self.send)
        send_button.place(x=520,y=380,width=60,height=40)

        self.chatbox.tag_config('tag3', foreground='green')
        self.chatbox.tag_config('tag4', foreground='blue')

        for i in self.msglist:
            if '~' in i:
                usertimer,ttaagg = i.split('~')
                self.chatbox.insert(tkinter.END, usertimer, 'tag3')
            else:
                self.chatbox.insert(tkinter.END, i)


    def send(self):
        message = self.chat_entry.get() + '~' + self.user + '~' + chat
        self.s.sendto(message.encode(), self.ip_port)
        print("already_send message:", message)
        return 'break'  # 按回车后�?发送不换�??

    def receive(self):
        global uses
        while True:
            data = self.s.recv(1024)
            data = data.decode()
            print("rec_data:", data)

            try:
                uses = json.loads(data)
                users.append('------Group chat-------')
            except:
                data = data.split('~')
                print("data_after_slpit:", data)  # data_after_slpit: ['cccc', 'a', '0/1']
                userName = data[0]  # data
                userName = userName[1:]
                message = data[1]  # name
                chatwith = data[2]  # destination
                message = '  ' + message + '\n'
                recv_time = " " + userName + "   " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': ' + '\n'
                self.chatbox.tag_config('tag3', foreground='green')
                self.chatbox.tag_config('tag4', foreground='blue')
                if chatwith == '0':  # 群聊
                    self.msglist.append(str(recv_time + '~' + 'tag3'))
                    self.msglist.append(str(message))

                    self.chatbox.insert(tkinter.END, recv_time, 'tag3')
                    self.chatbox.insert(tkinter.END, message)
                # elif chatwith != '0':  # 私聊�?人或�?�?己发出去的�?�聊
                #     if userName == user:  # 如果�?�?己发出去�?,用�?�聊字体显示
                #         self.chatbox.insert(tkinter.END, recv_time, 'tag3')
                #         self.chatbox.insert(tkinter.END, message, 'tag4')
                #     if chatwith == user:  # 如果�?发给�?己的，用绿色字体显示
                #         self.chatbox.insert(tkinter.END, recv_time, 'tag3')
                #         self.chatbox.insert(tkinter.END, message, 'tag4')
                self.chatbox.see(tkinter.END)
# ManagerView()
# root2.mainloop()