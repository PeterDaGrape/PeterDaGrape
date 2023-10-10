import socket

terminate = False

HOST = "172.20.10.13"
PORT = 39128



while True:

        rawmsg = input("send message request, TERMINATE to stop.   ")

        client = socket.socket(socket.AF_INET,
        socket.SOCK_STREAM)
        client.connect((HOST, PORT))   # Will connec with the server
                
        msg = rawmsg.encode()
        client.send(msg)
        from_server = client.recv(4096)
        print(from_server.decode())
        client.close()


