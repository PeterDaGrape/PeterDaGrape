import socket
import sys
HOST = "192.168.68.121"
PORT = 39127

client = socket.socket(socket.AF_INET,
socket.SOCK_STREAM)
client.connect((HOST, PORT))   # Will connect with the server
inArgument = (sys.argv[1])

print(inArgument)
msg = inArgument
client.send(msg.encode())
from_server = client.recv(4096)

