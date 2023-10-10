
import socket


data = "Hello World"

PORT = 39128

addr = "172.20.10.13"








serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind((addr, PORT))
serv.listen(5)
print('Listening on', addr)



while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
        rawdata = conn.recv(4096)
        data = rawdata.decode()
        if not data: break
        from_client += data
        print(from_client)
      
        conn.send("RECEIVED")
    conn.close()
    print('client disconnected')
