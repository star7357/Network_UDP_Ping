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

def pktDecoder(data) :
    rawData = data.decode('utf-8')
    pktSeqNo, message = rawData.split(DELIMITER)
    return pktSeqNo, message

def pktEncoder(pktSeqNo, message) :
    pkt = str(pktSeqNo) + DELIMITER + message
    return pkt.encode('utf-8')

def pingTestReport() :
    print("\n[ 10 Ping Packets Result ]\n")
    print("Ping Sent : %d" % sentPing)
    print("Ping Received : %d" % recvPing)
    print("Ping Lost : %d" % lostPing)
    print("Lost Ratio : %.2f" % round(lostRatio, 2))
    print("minRTT : %d ms, maxRTT : %d ms, avgRTT : %d ms\n" % (minRTT, maxRTT, avgRTT))

timeoutInterval = 1000
sentPing = 0
recvPing = 0
lostPing = 0
lostRatio = 0.0
minRTT = 2 * timeoutInterval
maxRTT = 0
sumRTT = 0
avgRTT = 0.0
message = "PING"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


for i in range(10) :
    sock.settimeout(timeoutInterval / 1000)
    try :
        pktSeqNo = str(i)

        startTime = now()
        sock.sendto(pktEncoder(pktSeqNo,message), (serverIP, serverPort))
        print ("\n%s %s sent" % (message, pktSeqNo))
        sentPing += 1

        # Waiting for packet response from the server with the same sequence number as pktSeqNo for 'timeout' time
        while True :
            data, addr = sock.recvfrom(1024)
            recvPktSeqNo, recvMessage = pktDecoder(data)
            print("Received Packet : (%s,%s)" % (recvPktSeqNo, recvMessage))
            
            # Check if the packet received was expected one
            if recvPktSeqNo == pktSeqNo : # If so, calculate the RTT
                endTime = now()
                RTT = endTime - startTime
                recvPing += 1
                sumRTT += RTT
                minRTT = min(RTT,minRTT)
                maxRTT = max(RTT,maxRTT)
                avgRTT = sumRTT / recvPing

                print("%s %s reply received from %s : RTT = %d ms" % (recvMessage, recvPktSeqNo, addr[0], RTT))
                break
            else : # Not expected packet received. Ignore the packet by substracting the elapsed time from default timeoutInterval and wait next packet
                elapsedTime = now() - startTime
                remainTime = timeoutInterval - elapsedTime
                sock.settimeout(remainTime / 1000)
                continue

    except socket.timeout :
        print("Time out!!!!")
        lostPing += 1
        lostRatio = lostPing / sentPing

pingTestReport()