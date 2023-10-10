import socket

terminate = False

HOST = "192.168.68.121"
PORT = 39127



while terminate == False:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))   # Will connect with the server
    msg = input("send message request, TERMINATE to stop.")
    if msg == "TERMINATE":
        exit()
    client.send(msg.encode())
    from_server = client.recv(4096)
    client.close()
    print(from_server.decode())
