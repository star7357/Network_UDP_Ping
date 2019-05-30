# client_skel.py
import socket
import random
import signal, sys
import ipaddress, getopt
import time

DELIMITER = '\n'

serverIP = 'nsl2.cau.ac.kr'
serverPort = 34367

now = lambda: int(round(time.time() * 1000))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

def pktDecoder(data) :
    rawData = data.decode('utf-8')
    pktSeqNo, message = rawData.split(DELIMITER)
    return pktSeqNo, message

def pktEncoder(pktSeqNo, message) :
    pkt = str(pktSeqNo) + DELIMITER + message
    return pkt.encode('utf-8')

message = "PING"
sentPkt = 0
recvPkt = 0
lostPkt = 0
lostRatio = 0.0
minRTT = 0
maxRtt = 0
avgRtt = 0.0

for i in range(10) :
    try :
        pktSeqNo = i
#       pktSeqNo = random.randrange(0, 9)

        startTime = now()
        sock.sendto(pktEncoder(pktSeqNo,message), (serverIP, serverPort))
        print ("Client: send \"" + message + "\", pktNo : " + str(pktSeqNo))
        sentPkt += 1

        while True :
            data, addr = sock.recvfrom(1024)
            recvPktSeqNo, recvMessage = pktDecoder(data)

            if recvPktSeqNo == pktSeqNo :
                endTime = now()
                RTT = endTime - startTime
                print("Packet (%s,%s) has been received successfully. RTT : %dms" % (recvPktSeqNo, recvMessage, RTT))
            else :
                continue

#        a,b = pktDecoder(data)

 #       print ("Client: recv \"" + b + "\", pktNo : " + str(a))
    except socket.timeout :
        print("Time out!!!!")

        pass
