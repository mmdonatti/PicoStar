#!/usr/bin/python

import socket
import signal
import sys
import time 
 
def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    s.close()
    sys.exit(0)
 
signal.signal(signal.SIGINT, signal_handler)
 
ECHO_SERVER_ADDRESS = "10.2.111.52"
ECHO_PORT = 4747
message = 'Hello, world'
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((ECHO_SERVER_ADDRESS, ECHO_PORT))
 
print 'Sending', repr(message) 
s.sendall(message)
#s.close()

time.sleep(5)

print 'Reconnecting'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ECHO_SERVER_ADDRESS, ECHO_PORT))
 
print 'Sending', repr(message) 
s.sendall(message)
s.close()
