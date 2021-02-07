from socket import *
import os
import threading
import requests
import time
import sys



userlist = {}
roomlist = {}
nicklist = []
globalchatlist = []

def user_handle(clnick, clsocket):
    while True:
        rcvd = clsocket.recv(1024)
        msg = rcvd.decode()
        print(clnick+': '+msg)
        if msg == '/createroom':
            if is_room_exist(clnick) == False:
                roomlist[clnick] = None
                clsocket.send('Successfully created your room. You are now unable to access global chat.'.encode())
                msg = '[Global]: '+clnick+' has created room.'
                globalchat(clnick, msg)
                globalchatlist.remove(clnick)
            else: clsocket.send('You are already in room.'.encode())
        elif msg == '/joinroom':
            if is_room_exist(clnick) == True: clsocket.send('You are already in room.'.encode())    
            else:
                clsocket.send('Enter the nickname who are in the room.'.encode())
                rcvd = clsocket.recv(1024)
                op = rcvd.decode()
                if is_room_exist(op) == True:
                    if roomlist[op] != None:
                        clsocket.send('That room is full.'.encode())
                    else:
                        roomlist[op] = clnick
                        roomlist[clnick] = op
                        opsocket = userlist[op]
                        realmsg = 'You have joined '+op+'\'s room.'
                        realmsgop = clnick+' has joined your room.'
                        opsocket.send(realmsgop.encode())
                        clsocket.send(realmsg.encode())
                        globalchatlist.remove(clnick)
                else: clsocket.send('There is no such room.'.encode())                  
        elif msg == '/disconnect': 
            if is_room_exist(clnick) == True:
                clsocket.send('You should use /quitroom first.'.encode())
            else: break
        elif msg == '/quitroom':
            if is_room_exist(clnick) == True:
                op = roomlist[clnick]
                if op != None:
                    opsocket = userlist[op]                  
                    roomlist[op] = None
                    realmsgop = clnick+' has quitted.'
                    opsocket.send(realmsgop.encode())
                globalchatlist.append(clnick)
                del roomlist[clnick]
                clsocket.send('You have quitted the room. You are now able to access global chat.'.encode())
            else: clsocket.send('You are not in room currently.'.encode())       
        elif msg =='/whoisroom':
            if is_room_exist(clnick) == True:
                op = roomlist[clnick]
                if op != None:
                    realmsg = op+' is in the room with you.'
                    clsocket.send(realmsg.encode())
                else:
                    clsocket.send('No one is in your room.'.encode())
            else: clsocket.send('You are not in room currently.'.encode())
        elif msg == '/roomlist':
            clsocket.send(str(roomlist).encode())
        elif msg == '/help':
            clsocket.send('/createroom : Create your room.\n/joinroom : Join someone\'s room.\n/quitroom : Quit your current room.\n/roomlist : Get current room list.\n/whoisroom : Print your opponent in your room.\n/disconnect : Disconnect from the server.\n/help : Get commands.\n'.encode())
        else:
            if is_room_exist(clnick) == True:
                op = roomlist[clnick]
                opsocket = userlist[op]
                realmsg = '[Local] '+clnick+': '+msg
                clsocket.send(realmsg.encode())
                opsocket.send(realmsg.encode())
            else:
                realmsg = '[Global] '+clnick+': '+msg
                globalchat(clnick, realmsg)
                
                    
    nicklist.remove(clnick)
    del userlist[clnick]
    clsocket.close()


def globalchat(clnick, msg):
    for user in userlist.keys():
        if user in globalchatlist:
            usersocket = userlist[user]          
            usersocket.send(msg.encode())
            print('send check')



def is_nick_exist(clnick):
    try:
        nicklist.index(clnick)
        return True
    except ValueError:
        return False


def is_room_exist(clnick):
    if clnick in roomlist:
        return True
    else:
        return False


def accept_wait(svSocket):
    while True:
        cnntSocket, addr = svSocket.accept()

        clnick = cnntSocket.recv(1024)
        clnick = clnick.decode()
        try:
            nicklist.index(clnick)
            cnntSocket.send('Duplicated Nickname. Pls try again.'.encode())
            cnntSocket.close()
        except ValueError:
            userlist[clnick] = cnntSocket
            nicklist.append(clnick)
            globalchatlist.append(clnick)
            handle_thread = threading.Thread(target=user_handle, args=(clnick, cnntSocket))
            handle_thread.daemon = True
            handle_thread.start()
        print(str(addr[0])+' connected. '+clnick+'\n')

  
exip = requests.get('https://api.ipify.org')
print('\nServer is now open. Enter \'server off\' to close the server.\n')
print('Your internal ip: '+gethostbyname(getfqdn())+'\n')
print('Your external ip: '+exip.text+'\n')
svSocket = socket(AF_INET, SOCK_STREAM)
svSocket.bind(('', 8080))
svSocket.listen(5)
accept_thread = threading.Thread(target=accept_wait, args=(svSocket,))
accept_thread.daemon = True
accept_thread.start()

while True:
    msg = input('')
    if msg == '/server off':
        print('Closing server...')
        try:
            for user in userlist.values():
                user.close()
        except:
            sys.exit()
        sys.exit()




    



            
        








