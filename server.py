from socket import *
import threading
import queue
import json  # json.dumps(some)打包  json.loads(some)解包

IP = '127.0.0.1'
PORT = 8000
messages = queue.Queue()
users = []# 0:userName 2:str(Client_IP)  3:int(Client_PORT)
lock = threading.Lock()
BUFLEN = 512

def Current_users():  # 统�?�当前在线人员，用于显示名单并发送消�?
    current_suers = []
    for i in range(len(users)):
        current_suers.append(users[i][0])      #存放用户相关名字
    return  current_suers

class ChatServer(threading.Thread):
    global users, que, lock
    def __init__(self):
        threading.Thread.__init__(self)
        self.s = socket(AF_INET,SOCK_DGRAM)

    def Load(self, data, addr):
        lock.acquire()
        try:
            messages.put((addr, data))
            print(f"Load,addr:{addr},data:{data}")
        finally:
            lock.release()
    def receive(self):
        while True:
            info,addr = self.s.recvfrom(1024)
            info_str = str(info,'utf-8')
            userIP = addr[0]
            userPort = addr[1]
            print(f'Info_str:{info_str},addr:{addr}')

            if '~0' in info_str:  # 群聊
                data = info_str.split('~')
                print("data_after_slpit:", data)  # data_after_slpit: ['cccc', 'a', '0']
                message = data[0]  # data
                userName = data[1]  # name
                chatwith = data[2]  # 0
                message = userName + '~' + message + '~' + chatwith  # 界面输出用户格式
                print("message:", message)
                self.Load(message, addr)
            # elif '~' in info_str and '0' not in info_str:  # 私聊
            #     data = info_str.split('~')
            #     print("data_after_slpit:", data)  # data_after_slpit: ['cccc', 'a', 'destination_name']
            #     message = data[0]  # data
            #     userName = data[1]  # name
            #     chatwith = data[2]  # destination_name
            #     message = userName + '~' + message + '~' + chatwith  # 界面输出用户格式
            #     self.Load(message, addr)
            else:  # 新用�?
                tag = 1
                temp = info_str
                for i in range(len(users)):  # 检验重名，则在重名用户后加数字
                    if users[i][0] == info_str:
                        tag = tag + 1
                        info_str = temp + str(tag)
                users.append((info_str, userIP, userPort))
                print("users:", users)  # 用户名和信息[('a', '127.0.0.1', 65350)]
                info_str = Current_users()  # 当前用户列表
                print("USERS:", info_str)  # ['a']
                self.Load(info_str, addr)

    def sendData(self):  # 发送数�?
        print('send')
        while True:
            if not messages.empty():  # 如果信息不为�?
                message = messages.get()
                print("messages.get()", message)
                if isinstance(message[1], str):  # 判断类型�?否为字�?�串
                    print("send str")
                    for i in range(len(users)):
                        data = ' ' + message[1]
                        print("send_data:", data.encode())  # send_data:b' a:cccc~a~------Group chat-------'
                        self.s.sendto(data.encode(), (users[i][1], users[i][2]))  # 聊天内�?�发送过�?

                if isinstance(message[1], list):  # �?否为列表
                    print("message[1]", message[1])  # message[1]为用户名 message[0]为地址元组
                    data = json.dumps(message[1])
                    for i in range(len(users)):
                        try:
                            self.s.sendto(data.encode(), (users[i][1], users[i][2]))
                            print("send_already")
                        except:
                            pass
        print('out send message loop')
    def run(self):
        self.s.bind((IP, PORT))         #绑定�?�?
        q = threading.Thread(target=self.sendData)  #开�?发送数�?线程
        q.start()
        t = threading.Thread(target=self.receive)  # 开�?接收信息进程
        t.start()

if __name__ == '__main__':
    print('start')
    cserver = ChatServer()
cserver.start()