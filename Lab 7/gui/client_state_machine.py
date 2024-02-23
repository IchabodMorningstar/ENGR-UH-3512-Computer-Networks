"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
import secrets

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

        self.private_key = secrets.randbits(10)
        #base
        self.base_key=1700
        #clock size
        self.clock_key=1901
        self.shared_key=None
        self.shared_keys=[]
        

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me


    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                        public_private_key = self.produce_public_private_key()
                        mysend(self.s, json.dumps(
                            {"action": "produce_public_private_keys", "target": self.peer, "message": public_private_key}
                        ))
                        
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    a=len(term)
                    
                    search_rslt1=''
                    for i in self.shared_keys:
                        term1=self.encrypt1(term,i)
                        mysend(self.s, json.dumps({"action":"search", "target":term1}))
                        search_rslt = json.loads(myrecv(self.s))["results"].strip()
                        rslt=search_rslt.split('\n')
                        b=len(rslt)
                        c=0
                        while c<b:
                            rslt[c]=rslt[c].split(":")
                            c+=1
                        print(rslt)
                        for k in rslt:
                            search_rslt1+=k[0]+k[1]+':'+self.decrypt1(k[2],i)+'\n'
                    # search_rslt=search_rslt[:-a]+self.decrypt(search_rslt[-a:])
                    
                    print(search_rslt1)
                    print(self.shared_keys)
                    if (len(search_rslt1)) > 0:
                        self.out_msg += search_rslt1 + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    # print(poem)
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                encrypted_msg=self.encrypt(my_msg)
            
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":encrypted_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"

                elif peer_msg['action']=="exchange":
                    decrypted_msg=self.decrypt(peer_msg['message'])
                    self.out_msg += peer_msg["from"]+decrypted_msg

                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                
                elif peer_msg["action"]=="produce_public_private_keys":
                    public_private_key=self.produce_public_private_key()
                    mysend(self.s, json.dumps(
                            {"action": "produce_shared_keys", "target": self.peer, "message": public_private_key}
                        ))
                    peer_public_private_key=int(peer_msg["message"])
                    self.shared_key = self.produce_shared_key(peer_public_private_key)
                    self.shared_keys.append(self.shared_key)
                    print("Your messages are encrypted. ")

                elif peer_msg["action"]=="produce_shared_keys":
                    peer_public_private_key=int(peer_msg["message"])
                    self.shared_key=self.produce_shared_key(peer_public_private_key)
                    self.shared_keys.append(self.shared_key)
                    print("Your messages are encrypted. ")
                

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg

    def produce_public_private_key(self):
        return self.base_key**self.private_key%self.clock_key

    def produce_shared_key(self, public_private_key):
        self.shared_key=public_private_key**self.private_key%self.clock_key
        return self.shared_key

    def encrypt(self, msg):
        encrypted_msg = ""
        for digit in msg:
            if digit == " ":
                encrypted_msg += " "
            else:
                encrypted_msg += chr(ord(digit)+self.shared_key)
        return encrypted_msg

    def encrypt1(self, msg, shared_key):
        encrypted_msg = ""
        for digit in msg:
            if digit == " ":
                encrypted_msg += " "
            else:
                encrypted_msg += chr(ord(digit)+shared_key)
        return encrypted_msg

    def decrypt(self, encrpted_msg):
        decrypted_msg = ""
        for digit in encrpted_msg:
            if digit == " ":
                decrypted_msg += " "
            else:
                decrypted_msg += chr(ord(digit)-self.shared_key)
        return decrypted_msg

    def decrypt1(self, encrpted_msg, shared_key):
        decrypted_msg = ""
        for digit in encrpted_msg:
            if digit == " ":
                decrypted_msg += " "
            else:
                decrypted_msg += chr(ord(digit)-shared_key)
        return decrypted_msg
