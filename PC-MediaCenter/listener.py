import time
from socket import * # socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname
import sys

import win32api
import win32con
import win32com

volume = 100

def keyPress(key) :
    win32api.keybd_event(key, 0,0,0)
    time.sleep(.0001)
    win32api.keybd_event(key, 0,win32con.KEYEVENTF_KEYUP,0)

def processCmd(inputBuff):
    global volume
    j = 0
    CmdCount = 0
    while j < len(inputBuff) :
        CmdCount = CmdCount+1
        i = inputBuff[j]
        print('Command: {0}, buff index: {1}'.format(inputBuff[j],j))
        if   i == 'p' :
             keyPress(win32con.VK_MEDIA_PLAY_PAUSE)
        elif i == 'n' :
             keyPress(win32con.VK_MEDIA_NEXT_TRACK) 
        elif i == 'b' :
             keyPress(win32con.VK_MEDIA_PREV_TRACK)
        elif i == 'm' :
             keyPress(win32con.VK_VOLUME_MUTE)
        elif i == 'v' :
            diff = volume - ord(inputBuff[j+1])
            j = j+1
            volume = volume - diff
            while diff > 1 :
                keyPress(win32con.VK_VOLUME_DOWN)
                diff = diff - 2;
            while diff < -1 :
                keyPress(win32con.VK_VOLUME_UP)
                diff = diff + 2;
            volume = volume + diff
            print('Expected volue: {0}'.format(volume))
        j = j + 1
    print('FINISHED, Executed {0} commands.'.format(CmdCount))



PORT_NUMBER = 5000
CommandCenterPortBcast = 5001
SIZE = 1024

hostName = gethostname()

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

print ("Server listening on host:{1}\n IP:{2}\n Port {0}\n".format(PORT_NUMBER,hostName,gethostbyname(hostName)))
cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
cs.bind((hostName,CommandCenterPortBcast))
time.sleep(1) 
cs.sendto(b'This is a test', ('192.168.1.255', CommandCenterPortBcast))

while True:
        data = 0;
        cmds = b''
        (data,addr) = mySocket.recvfrom(SIZE)
        mySocket.setblocking(0);
        try:
            while(data != None):
                cmds += data
                (data,addr) = mySocket.recvfrom(SIZE)
        except BlockingIOError:
            cmds = cmds
        mySocket.setblocking(1);
        print(cmds)
        processCmd(cmds.decode("utf-8"))
sys.exit()