import time
from socket import * # socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname
import sys
import threading

import winVolume

import win32api
import win32con
import win32com
import pyHook
import pythoncom


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


def keyPress(key,shift=False) :
    if shift:        
        win32api.keybd_event(win32con.VK_SHIFT, 0,0,0)
        time.sleep(.0001)
    win32api.keybd_event(key, 0,0,0)
    time.sleep(.0001)
    win32api.keybd_event(key, 0,win32con.KEYEVENTF_KEYUP,0)
    if shift:
        win32api.keybd_event(win32con.VK_SHIFT, 0,win32con.KEYEVENTF_KEYUP,0)

def MouseRightClick() :
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(.0001)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

def MouseLeftClick() :
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.0001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def moveMouse(x,y):
    
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,x,y)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,x,y)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,x,y)

def processCmd(inputBuff):
    global volume
    j = 0
    CmdCount = 0
    while j < len(inputBuff) :
        CmdCount = CmdCount+1
        i = inputBuff[j]
        print('Command: {0}, buff index: {1}'.format(inputBuff[j],j))
        if   i == b'p'[0] :
             keyPress(win32con.VK_MEDIA_PLAY_PAUSE)
        elif i == b'n'[0] :
             keyPress(win32con.VK_MEDIA_NEXT_TRACK) 
        elif i == b'b'[0] :
             keyPress(win32con.VK_MEDIA_PREV_TRACK)
        elif i == b'm'[0] :
             keyPress(win32con.VK_VOLUME_MUTE)
        elif i == b'v'[0] and len(inputBuff) > j+1:
            newVol = inputBuff[j+1]
            if(newVol >= 0 or newVol <= 100) :
                #print('Going from volume: {0} to {1}'.format(int(volume.GetMasterVolumeLevelScalar()*100),newVol))
                volume.SetMasterVolumeLevelScalar(newVol/100,None)
            j = j+1
        elif i == b't'[0] and len(inputBuff) > j+4:
            x  = inputBuff[j+1]
            y  = inputBuff[j+2]
            if x > 127 :
                x -= 256
            if y > 127 :
                y -= 256
            #print(str(x)+' '+str(y))
            moveMouse(x,y)
            j += 2
        elif i == b'l'[0]:
            MouseLeftClick()
        elif i == b'r'[0]:
            MouseRightClick()            
        elif i == b'k'[0] and len(inputBuff) > j+1:
            print(inputBuff[j+1:])
            for k in range(j+2,j+2+inputBuff[j+1]) :
                c = chr(inputBuff[k])
                shift = False
                if c.isnumeric() :
                    c = 0x30 + int(c)
                elif c.isupper() :
                    shift = True
                    c = 0x41 + ord(c.lower()) - ord('a'[0])
                else :
                    c = 0x41 + ord(c)-ord('a')
                keyPress(c,shift)
                j += 1
            j += 1
        j = j + 1
    #print('FINISHED, Executed {0} commands.'.format(CmdCount))

hostName = gethostname()
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )
spam = IdSpam(mySocket.getsockname()[1])
spam.start()
print ("Server listening on host:{1}\n IP:{2}\n Port {0}\n".format(mySocket.getsockname()[1],hostName,gethostbyname(hostName)))

while True:
        data = b'';
        cmds = b''
        #(data,addr) = mySocket.recvfrom(SIZE)
        mySocket.setblocking(0);
        try:
            while(data != None):
                cmds += data
                (data,addr) = mySocket.recvfrom(SIZE)
        except BlockingIOError:
                pass #cmds = cmds
        mySocket.setblocking(1);
        processCmd(cmds)
sys.exit()
