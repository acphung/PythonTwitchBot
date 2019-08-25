from dotenv import load_dotenv
import os
import socket

load_dotenv()
HOST = "irc.chat.twitch.tv"
PORT = 6667

print("Running Bot...", flush=True)

irc = socket.socket()
irc.connect((HOST, PORT))
irc.send(("PASS " + os.getenv("TWITCH_AUTH") + "\r\n").encode())
irc.send(("NICK " + os.getenv("TWITCH_NICK") + "\r\n").encode())

while True:
    msg = irc.recv(2048).decode()
    if msg.find("PING") != -1:
        print("Received Ping!\nSending Pong Back!", flush=True)
        irc.send(("PONG :tmi.twitch.tv\r\n").encode())
        break
    elif msg.find(":>") != -1:
        print(msg, flush=True)
        # break

print()
print("SUCCESSFULLY CONNECTED TO TWITCH IRC")
