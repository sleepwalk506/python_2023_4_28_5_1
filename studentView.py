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
root2.title('Student')

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

class StudentView():
    def __init__(self,STUIP,STUPORT,user):
        self.user = user
        self.STUIP = STUIP
        self.STUPORT = STUPORT
        self.user = user
        print(STUIP,STUPORT)
        self.msglist = []
        self.createPage()


    def createPage(self):
        self.show_all_frame = tk.Frame(root2)

        self.query_bar_frame = tk.Frame(root2)
        self.course_select_frame = tk.Frame(root2)

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

        menubar.add_command(label='查�??',command=self.query_bar)
        menubar.add_command(label='选�??',command=self.courseSelection)

        menubar.add_command(label='交流',command=self.chat_bar)
        root2['menu'] = menubar

        root2.mainloop()

    def show_all(self):
        self.chat_frame.destroy()
        self.show_all_frame = tk.Frame(root2)
        self.show_all_frame.pack()
        self.course_select_frame.destroy()
        self.query_bar_frame.destroy()

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



    def query_bar(self):
        self.chat_frame.destroy()
        self.query_bar_frame = tk.Frame(root2)
        self.show_all_frame.destroy()
        self.course_select_frame.destroy()
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

    def courseSelection(self):
        self.chat_frame.destroy()
        self.query_bar_frame.destroy()
        self.show_all_frame.destroy()
        self.course_select_frame = tk.Frame(root2)
        self.course_select_frame.pack()
        self.course_select_frame.place(x=0, y=30, width=640, height=440)

        tk.Label(self.course_select_frame,text='选择课程编号').place(x=140, y=20, width=100, height=40)
        self.course_select_entry = tk.Entry(self.course_select_frame)
        self.course_select_entry.place(x=240, y=25, width=120, height=30)

        course_select_button = tk.Button(self.course_select_frame, text='选�??',command=self.select_commit)
        course_select_button.place(x=370, y=25, width=40, height=30)

    def select_commit(self):
        # successLabel = tk.Label(text="选�?�成�?")
        # failLabel = tk.Label(text="课程人数已满，选�?�失�?")

        courseNumber = self.course_select_entry.get()
        result = cursor.execute("select currNumber from courseselection where courseNumber=%s",courseNumber)
        if result:
            currN = cursor.fetchall()
            currN = currN[0][0]

            cursor.execute("select maxNumber from courseselection where courseNumber=%s", courseNumber)
            maxN = cursor.fetchall()
            maxN = maxN[0][0]

            currN = int(currN)
            maxN = int(maxN)
            # print(currN, maxN)

            if currN < maxN:
                currN += 1
                # values = [currN, courseNumber]
                cursor.execute(f"update courseselection set currNumber={currN} where courseNumber={courseNumber}")
                db.commit()
                tk.Label(self.course_select_frame, text="选�?�成�?").place(x=200, y=100, width=150, height=40)
            else:
                tk.Label(self.course_select_frame, text="课程人数已满，选�?�失�?").place(x=200, y=100, width=150,
                                                                                       height=40)
        else:
            tk.Label(self.course_select_frame, text="课程不存�?").place(x=200, y=100, width=150, height=40)

    def chat_bar(self):

        self.query_bar_frame.destroy()
        self.show_all_frame.destroy()
        self.chat_frame = tk.Frame(root2)
        self.chat_frame.pack()
        self.course_select_frame.destroy()
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

# StudentView('1','1')
# root2.mainloop()