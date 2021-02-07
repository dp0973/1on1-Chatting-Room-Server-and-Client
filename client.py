from socket import *
import os
import sys
import threading
import chess
import time

print('Make sure your port 8080 is open.\n\n')
nick = input('Set Nickname: ')
ip = input('Server IP: ')

def sendmsg(socket, nick):
    while True:
        msg = input('')
        socket.send(msg.encode())

def rcvmsg(socket, nick):
    while True:
        msg = socket.recv(1024)
        print(msg.decode(),'\n')


print('Requesting connection to '+ip+'...')
clSocket = socket(AF_INET, SOCK_STREAM)
clSocket.connect((ip, 8080))

print('Connection with '+ip+' success! **Use /help to get commands.**\n')
clSocket.send(nick.encode())

sendt = threading.Thread(target=sendmsg, args=(clSocket, nick))
rcvt = threading.Thread(target=rcvmsg, args=(clSocket, nick))

sendt.start()
rcvt.start()
