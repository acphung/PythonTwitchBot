from dotenv import load_dotenv
import os
import socket

load_dotenv()
HOST = "irc.chat.twitch.tv"
PORT = 6667
DEBUG = True


def printFlush(msg=""):
    print(msg, flush=True)


def sendMsg(msg=""):
    irc.send((msg + "\r\n").encode())


def recvMsg():
    return irc.recv(2048).decode()


printFlush("Running Bot...")

irc = socket.socket()
irc.settimeout(30)
irc.connect((HOST, PORT))
sendMsg("PASS " + os.getenv("TWITCH_AUTH"))
sendMsg("NICK " + os.getenv("TWITCH_NICK"))

while True:
    try:
        msg = recvMsg()
    except socket.timeout:
        printFlush("ERROR: The Socket Timeout!")
        msg = ""

    if DEBUG:
        printFlush("DEBUG: [ " + msg + " ]")

    if msg.find("PING") != -1:
        printFlush("*** Received Ping! Sending Pong Back!")
        sendMsg("PONG :tmi.twitch.tv")
        # break
    elif msg.find(":>") != -1:
        printFlush(msg)
        printFlush()
        printFlush("*** SUCCESSFULLY CONNECTED TO TWITCH IRC!")
        printFlush("*** Attempting to Join Channel...")
        sendMsg("JOIN #zyfae")
    elif msg.find(":End of /NAMES list") != -1:
        # printFlush(msg)
        sendMsg("PRIVMSG #zyfae :Hello, This is Test Bot!")
    elif msg.find("PRIVMSG") != -1:
        printFlush(msg)
        if msg.find("!shutdown") != -1:
            sendMsg("PRIVMSG #zyfae :Bot is shutting down!")
            sendMsg("PART #zyfae")
    elif msg.find("PART") != -1:
        printFlush("*** Bot has successfully left the channel!")
        break

printFlush("*** Bot is now shutting down!")
irc.close()
