import socket

HOST = "192.168.68.121"
PORT = 39127

client = socket.socket(socket.AF_INET,x
socket.SOCK_STREAM)
client.connect((HOST, PORT))   # Will connect with the server

msg = "CLEAR"
client.send(msg.encode())
from_server = client.recv(4096)
client.close()
print(from_server.decode())
