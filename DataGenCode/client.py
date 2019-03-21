import socket
import atexit
import time

###
# Client class to establish connection  
# to the microcontroller via AF_INET
# for understanding and examples:
# https://docs.python.org/2.7/library/socket.html
# #

def connect():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('169.254.26.67', 12506))

    return s