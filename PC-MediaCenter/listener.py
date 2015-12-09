import time
from socket import * # socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname
import sys
import threading

import winVolume

import win32api
import win32con
import win32com


PORT_NUMBER = 5001
CommandCenterPortBcast = 5002
SIZE = 1024
volume = winVolume.GetVolumeControl()

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
            self.cs.sendto(bytes(str(self.port),'utf-8'), ('255.255.255.255', CommandCenterPortBcast))
            time.sleep(5)


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
            newVol = ord(inputBuff[j+1])
            if(newVol >= 0 or newVol <= 100) :
                print('Going from volume: {0} to {1}'.format(int(volume.GetMasterVolumeLevelScalar()*100),newVol))
                volume.SetMasterVolumeLevelScalar(newVol/100,None)
            j = j+1
        j = j + 1
    print('FINISHED, Executed {0} commands.'.format(CmdCount))

hostName = gethostname()
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )
spam = IdSpam(mySocket.getsockname()[1])
spam.start()
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
        except BlockingIOError:
            cmds = cmds
        mySocket.setblocking(1);
        print(cmds)
        processCmd(cmds.decode("utf-8"))
sys.exit()