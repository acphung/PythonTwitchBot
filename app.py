from dotenv import load_dotenv
import os
import socket

load_dotenv()
HOST = "irc.chat.twitch.tv"
PORT = 6667

print("Running Bot...")

irc = socket.socket()
irc.connect((HOST, PORT))
irc.send(("PASS " + os.getenv("TWITCH_AUTH") + "\r\n").encode())
irc.send(("NICK " + os.getenv("TWITCH_NICK") + "\r\n").encode())

while True:
    msg = irc.recv(2048).decode()
    print(msg)
    # if msg.find(":>") != -1:
    #     print("CONNECTED")
    if msg.find(":>") != -1:
        break

print()
print("SUCCESSFULLY CONNECTED TO TWITCH IRC")
