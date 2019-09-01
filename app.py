from dotenv import load_dotenv
import os
import socket

# Getting the environment variable needed to authenticate the bot
load_dotenv()
HOST = "irc.chat.twitch.tv"
PORT = 6667
DEBUG = True

# --- Utility Functions --- #


def printFlush(msg=""):
    print(msg, flush=True)


def sendMsg(msg=""):
    irc.send((msg + "\r\n").encode())


def recvMsg():
    return irc.recv(2048).decode()

# --- Main --- #


# Start the bot & create the socket & connect to twitch irc server
printFlush("Running Bot...")
irc = socket.socket()
irc.settimeout(30)
irc.connect((HOST, PORT))
sendMsg("PASS " + os.getenv("TWITCH_AUTH"))
sendMsg("NICK " + os.getenv("TWITCH_NICK"))


# Start listening to twitch irc server
while True:
    try:
        msg = recvMsg()
    except socket.timeout:
        printFlush("ERROR: The Socket Timeout!")
        msg = ""

    if DEBUG:
        printFlush("DEBUG: [ " + msg + " ]")

    # Handle the various response from the server
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


# Closing the socket and ending the connection to the twitch irc server
printFlush("*** Bot is now shutting down!")
irc.close()
