'''
import subprocess
def set_master_volume(val):
    val = float(int(val))
    proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
    proc.wait()
while True:
    set_master_volume(int(input('make command string:')))
'''
import socket

SERVER = socket.gethostname()
PORT = 5000

#print([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]][:1])


mySocket = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
while True:
    mySocket.sendto(bytes(input('make command string:'),'utf-8'),(SERVER,PORT))
