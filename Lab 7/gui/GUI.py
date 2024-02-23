#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter.messagebox import *
from chat_utils import *
import json
import pickle

# GUI class for the chat


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""
        self.users={}

    def login(self):        
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Log in")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # create a Label
        self.pls = Label(self.login,
                         text="Welcome to Stay Fit",
                         justify=CENTER,
                         font="Gabriola 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.3,
                       rely=0.07)
        # create a Label        
        self.labelName = Label(self.login,
                               text="Username: ",
                               font="Gabriola 14 bold")
                               
        self.labelName.place(relheight=0.12,
                             relx=0.1, rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login, font="Gabriola 14 bold")
                               
        self.entryName.place(relwidth=0.3,
                             relheight=0.09,
                             relx=0.35,
                             rely=0.2)
        
        # create second Label        
        self.labelpsw = Label(self.login, text="Password:",
                               font="Gabriola 14 bold")

        self.labelpsw.place(relheight=0.12,
                             relx=0.1, rely=0.35)

        # create a entry box for
        # tyoing the message
        self.entrypsw = Entry(self.login, show="*",
                              font="Gabriola 14 bold")

        self.entrypsw.place(relwidth=0.3, relheight=0.09,
                             relx=0.35, rely=0.35)

        # set the focus of the curser
        self.entryName.focus()

        # create a Continue Button
        # along with action
        self.log_in = Button(self.login, text="Log in", font="Gabriola 14 bold", justify=CENTER,
                         command=lambda: self.goAhead(self.entryName.get(), self.entrypsw.get()))

        self.log_in.place(relwidth=0.15, relheight=0.09, relx=0.4, rely=0.47)
        
        self.sign_up = Button(self.login,
                         text="Sign up",
                         font="Gabriola 14 bold",
                         justify=CENTER,
                         command= self.signup)

        self.sign_up.place(relwidth=0.15, relheight=0.09, relx=0.4, rely=0.59)
        
        self.Window.mainloop()
        
    def signup(self):
        def joinsf():
            # getting new data
            np = new_pwd.get()
            npc = new_pwd_confirm.get()
            nn = new_name.get()
     
            # loading existing user data
            try:
                with open('usrs_info.pickle', 'rb') as usr_file:
                    usr_info = pickle.load(usr_file)
            except:
                with open('usrs_info.pickle', 'wb') as usr_file:
                    usr_info = {'Ichabod': 'crane'}
                    pickle.dump(usr_info, usr_file)
                    usr_file.close()
            #different psw
            if np != npc:
                showerror('Error', 'Password and confirm password must be the same!')
     
            # name exists
            elif nn in usr_info:
                showerror('Error', 'The user has already signed up!')
     
            # normal condition
            else:
                usr_info[nn] = np
                with open('usrs_info.pickle', 'wb') as usr_file:
                    pickle.dump(usr_info, usr_file)
                showinfo('Welcome', 'You have successfully signed up!')
                window_sign_up.destroy()
            
        window_sign_up = Toplevel(self.Window)
        window_sign_up.geometry('300x200')
        window_sign_up.title('Join Stay Fit')
     
        new_name = StringVar()  
        Label(window_sign_up, text='User name: ', font="Gabriola 14 bold").place(x=10, y=10) 
        entry_new_name = Entry(window_sign_up, textvariable=new_name, font="Gabriola 10 bold") 
        entry_new_name.place(x=155, y=10) 
     
        new_pwd = StringVar()
        Label(window_sign_up, text='Password: ', font="Gabriola 14 bold").place(x=10, y=50)
        entry_usr_pwd = Entry(window_sign_up, textvariable=new_pwd, show='*', font="Gabriola 10 bold")
        entry_usr_pwd.place(x=155, y=50)
     
        new_pwd_confirm = StringVar()
        Label(window_sign_up, text='Confirm password: ',font="Gabriola 14 bold").place(x=10, y=90)
        entry_usr_pwd_confirm = Entry(window_sign_up, textvariable=new_pwd_confirm, show='*', font="Gabriola 10 bold")
        entry_usr_pwd_confirm.place(x=155, y=90)
     
        btn_comfirm_sign_up = Button(window_sign_up, text='Sign up', font="Gabriola 12 bold", command=joinsf)
        btn_comfirm_sign_up.place(relwidth=0.3, relheight=0.13, x=150, y=120)

    def goAhead(self, name, psw):
        if len(name)>0 and len(psw)>0:
            try:
                with open('usrs_info.pickle', 'rb') as usr_file:
                    usr_info = pickle.load(usr_file)
            except:
                with open('usrs_info.pickle', 'wb') as usr_file:
                    usr_info = {'Ichabod': 'crane'}
                    pickle.dump(usr_info, usr_file)
                    usr_file.close()
            if name in usr_info.keys():
                if psw==usr_info[name]:
                    msg= json.dumps({"action": "login", "name": name})
                    self.send(msg)
                    response = json.loads(self.recv())
                    if response['status']=='ok':
                        self.login.destroy()
                        self.sm.set_state(S_LOGGEDIN)
                        self.sm.set_myname(name)
                        self.layout(name)
                        self.textCons.config(state=NORMAL)
                        # self.textCons.insert(END, "hello" +"\n\n")
                        self.textCons.insert(END, menu + "\n\n")
                        self.textCons.config(state=DISABLED)
                        self.textCons.see(END)
                        # while True:
                        #     self.proc()
                else:
                    showinfo(message='try again')
            else:
                showinfo(message='user not exits')
        # the thread to receive messages
        process = threading.Thread(target=self.proc)
        process.daemon = True
        process.start()

    # The main layout of the chat
    def layout(self, name):

        self.name = name
        
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470, height=545, bg="purple")
        
        # to have menu
        menubar=Menu(self.Window)
        funcmenu=Menu(menubar, tearoff=0)
        menubar.add_cascade(label='· · ·', menu=funcmenu)
        # add funcs to menu
        funcmenu.add_command(label='Add Contacts', command=lambda : self.nextmove('c'))
        funcmenu.add_command(label='Search Chat History', command=lambda : self.nextmove('?'))
        funcmenu.add_command(label='Who Are Online', command=lambda : self.nextmove('who'))        
        funcmenu.add_command(label='Time', command=lambda : self.nextmove('time'))
        funcmenu.add_command(label='Poem', command=lambda : self.nextmove('poem'))
        funcmenu.add_command(label='Quit', command=lambda : self.nextmove('quit'))
        self.Window.config(menu=menubar)
        
        self.labelHead = Label(self.Window,bg="cyan",fg="black",font="Gabriola 19 bold",text=self.name, pady=1)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="black")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="cyan",
                             fg="black",
                             font="Gabriola 14 bold",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="black",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="cyan",
                              fg="black",
                              font="Gabriola 15 bold")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.78,
                            relheight=0.03,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Gabriola 13 bold",
                                width=20,
                                bg="green",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.78,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages
    
    def nextmove(self, act):
        def go(act, cmd):
            self.my_msg=act[0]+cmd
            func_window.destroy()
        
        if act == "time":
            self.my_msg='time'
        elif act=='who':
            self.my_msg="who"
        elif act=="quit":
            self.my_msg="q"
        else:
            func_window = Toplevel(self.Window)
            func_window.geometry('150x100')
            func_window.title(act)
            
            new_move = StringVar()
            entry_nm = Entry(func_window, textvariable=new_move, font="Gabriola 10 bold")
            entry_nm.place(x=10, y=10)
         
            btn_nm = Button(func_window, text='go', font="Gabriola 12 bold", command=lambda: go(act, entry_nm.get()))
            btn_nm.place(relwidth=0.3, relheight=0.25, x=10, y=37)
    
    def sendButton(self, msg):
        # self.textCons.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, self.system_msg + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()


# create a GUI class object
if __name__ == "__main__":
    # g = GUI()
    pass
