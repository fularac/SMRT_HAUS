from socket import *
from time import sleep

# Defaults
myHostname= gethostname()
BroadcastPort= 5001

# Create socket to spam broadcast message.
cs = socket(AF_INET, SOCK_DGRAM)
cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
cs.bind(('192.168.1.255',BroadcastPort))

while True:
    cs.sendto('I am a SMRT HAUS Device!!!',('255.255.255.255',5001))#, #('192.168.1.255', BroadcastPort))
    sleep(5)
