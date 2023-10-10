import socket

HOST = "192.168.68.121"
PORT = 39127

client = socket.socket(socket.AF_INET,
socket.SOCK_STREAM)
client.connect((HOST, PORT))   # Will connect with the server

msg = "HEX 243 231 211"
client.send(msg.encode())
from_server = client.recv(4096)
client.close()
print(from_server.decode())
