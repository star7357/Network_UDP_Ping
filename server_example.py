# server_skel.py
import socket
import time, datetime
import random
from _thread import *
import signal, sys

DELIMITER = '\n'

server_ip = 'nsl2.cau.ac.kr'
server_port = 34367

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((server_ip, server_port))

def pktDecoder(data) :
    rawData = data.decode('utf-8')
    pktSeqNo, message = rawData.split(DELIMITER)
    return pktSeqNo, message

def pktEncoder(pktSeqNo, message) :
    pkt = str(pktSeqNo) + DELIMITER + message
    return pkt.encode('utf-8')

def pktProcessing(data, addr) :
    dict_recvPkts = dict()
    clientIP, clientPort = addr
    pktSeqNo, message = pktDecoder(data)
    delay = 2 * random.random()
    print("Message Delivered. Message : %s, PktNo : %s, (Delay : %.4f)" % (message, str(pktSeqNo), delay))

    # Packet from (clientIP,clientPort) has been arrived first time
    # Save CACK for each (IP,Port) 
    if addr not in dict_recvPkts :
        dict_recvPkts[(clientIP, clientPort)] = pktSeqNo
        time.sleep(delay)
        sock.sendto(pktEncoder(pktSeqNo,message),addr)
        print("Pkt sent.")
    else : # Packet from (clientIP, clientPort) has been arrived before at least once
        # SeqNo in packet is not bigger than CACK, it means the received packt is out-of-order
        if pktSeqNo <= dict_recvPkts[(clientIP, clientPort)] :
            print("The packet received is out-of-order.")
            return 
        else : # The packet from (IP,Port) has been received before, and the packet is in order
            dict_recvPkts[(clientIP,clientPort)] = pktSeqNo
            time.sleep(delay)
            sock.sendto(pktEncoder(pktSeqNo,message), addr)
            print("Pkt sent.")

while True :
    data,addr = sock.recvfrom(1024)
    if random.randrange(0,100) < 20 :
        continue
    else :
        start_new_thread(pktProcessing, (data,addr,))
