from dotenv import load_dotenv
import os
import socket
import re

# Getting the environment variable needed to authenticate the bot
load_dotenv()
HOST = "irc.chat.twitch.tv"
PORT = 6667
DEBUG = True
CHANNELS = ["zyfae"]

# --- Utility Functions --- #


def printFlush(msg=""):
    print(msg, flush=True)


def sendMsg(msg=""):
    irc.send((msg + "\r\n").encode())


def recvMsg():
    return irc.recv(2048).decode()


def getChannel(msg):
    # Returns the Chat Channel Name else returns None
    tokens = msg.split(":")[1:]
    result = re.search(r"#(.*)", tokens[0])
    if result:
        print(result.groups())
        return result.group(1)
    return None


def getCommand(msg):
    # Returns the name of the twitch irc command else returns None
    tokens = msg.split(":")[1:]
    result = re.search(r"[.*]* ([^ |\n]*) [.*]*", tokens[0])
    if result:
        print(result.groups())
        return result.group(1)
    return None


def getUsername(msg):
    # Returns the username else returns None
    tokens = msg.split(":")[1:]
    result = re.search(
        r"<([^ |\n]*)>!<([^ |\n]*)>@<([^ |\n]*)>.tmi.twitch.tv", tokens[0])
    if result:
        print(result.groups())
        return result.group(1)
    return None


def getMsg(msg):
    # Returns the message else returns None
    return msg.split(":")[1:][1]


def joinChannels(channels):
    # Join the twitch chat of each of the channel specified
    for channel in channels:
        if channel[0] != "#":
            channel = "#" + channel
        cmd = "JOIN " + channel
        sendMsg(cmd)
        try:
            msg = recvMsg()
        except socket.timeout:
            printFlush("ERROR: The Socket Timeout!")
            msg = ""

        if msg == "":
            if msg.find(":End of /NAMES list") != -1:
                printFlush("*** SUCCESSFULLY JOINED THE CHANNEL")
                sendMsg("PRIVMSG " + channel + " :Hello, This is a Test Bot!")


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
        msg = "listening..."

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
        printFlush("*** SUCCESSFULLY JOINED THE CHANNEL")
        sendMsg("PRIVMSG #zyfae :Hello, This is a Test Bot!")
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
