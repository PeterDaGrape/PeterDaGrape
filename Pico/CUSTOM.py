import socket

terminate = False

HOST = "192.168.1.121"
PORT = 39127



while True:

        rawmsg = input("send message request, TERMINATE to stop.   ")

        client = socket.socket(socket.AF_INET,
        socket.SOCK_STREAM)
        client.connect((HOST, PORT))   # Will connect with the server
                
        if rawmsg == 'DISCONNECT':
                client.close()

        elif rawmsg == 'CONNECT':
                client = socket.socket(socket.AF_INET,
                socket.SOCK_STREAM)
                client.connect((HOST, PORT))
        elif rawmsg == 'STOP':
                client.close
                exit()
        else:

                msg = rawmsg.encode()
                client.send(msg)
                from_server = client.recv(4096)
                print(from_server.decode())
                client.close()


