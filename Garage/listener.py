import time
from socket import * # socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname
import sys
import threading

import doorControl as door

PORT_NUMBER = 5000
CommandCenterPortBcast = 5002
SIZE = 1024

class IdSpam(threading.Thread):
    def __init__(self,port):
        threading.Thread.__init__(self)
        self.port = int(port)
        self.cs = socket(AF_INET, SOCK_DGRAM)
        self.cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.cs.bind((hostName,CommandCenterPortBcast))
    def run(self):
        while True:
            #self.cs.sendto(bytes(str(self.port),'utf-8'), ('255.255.255.255', CommandCenterPortBcast))
            time.sleep(5)



def processCmd(inputBuff):
    global volume
    j = 0
    CmdCount = 0
    while j < len(inputBuff) :
        CmdCount = CmdCount+1
        i = inputBuff[j]
        print('Command: {0}, buff index: {1}'.format(inputBuff[j],j))
        if   i == 'b' :
             door.HitButton()
        j = j + 1
    print('FINISHED, Executed {0} commands.'.format(CmdCount))

hostName = gethostname()
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( ('192.168.1.190', PORT_NUMBER) )
#spam = IdSpam(mySocket.getsockname()[1])
#spam.start()
door.init()
print ("Server listening on host:{1}\n IP:{2}\n Port {0}\n".format(mySocket.getsockname()[1],hostName,gethostbyname(hostName)))

while True:
        data = 0;
        cmds = b''
        (data,addr) = mySocket.recvfrom(SIZE)
        mySocket.setblocking(0);
        try:
            while(data != None):
                cmds += data
                (data,addr) = mySocket.recvfrom(SIZE)
                

        except error :#BlockingIOError:
            cmds = cmds
        mySocket.setblocking(1);
        print(cmds)
        processCmd(cmds.decode("utf-8"))
sys.exit()
