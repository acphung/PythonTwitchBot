from dotenv import load_dotenv
import os
import socket

load_dotenv()
HOST = "irc.chat.twitch.tv"
PORT = 6667


def printFlush(msg=""):
    print(msg, flush=True)


def sendMsg(msg=""):
    irc.send((msg + "\r\n").encode())


def recvMsg():
    return irc.recv(2048).decode()


printFlush("Running Bot...")

irc = socket.socket()
irc.connect((HOST, PORT))
sendMsg("PASS " + os.getenv("TWITCH_AUTH"))
sendMsg("NICK " + os.getenv("TWITCH_NICK"))

while True:
    msg = recvMsg()
    if msg.find("PING") != -1:
        printFlush("Received Ping!\nSending Pong Back!")
        sendMsg("PONG :tmi.twitch.tv")
        break
    elif msg.find(":>") != -1:
        printFlush(msg)

printFlush()
printFlush("SUCCESSFULLY CONNECTED TO TWITCH IRC!")
