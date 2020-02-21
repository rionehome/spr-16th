import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 50007))
while True:
    data = s.recv(1024)# the type of data is string
    print(data)
