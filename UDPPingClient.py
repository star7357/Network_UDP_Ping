#
# UDPPingClient.py
# StudentID : 20144367 Name : Lee,Donghyun
#
import socket
import random
import signal, sys
import ipaddress, getopt
import time

DELIMITER = '\n'

serverIP = 'nsl2.cau.ac.kr'
serverPort = 34367
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

# Signal handler for input'Ctrl + C'
def signal_handler(signal, frame): 
    print('Bye bye~')
    sock.close()
    sys.exit(0)

now = lambda: int(round(time.time() * 1000))

def pktDecoder(data) :
    rawData = data.decode('utf-8')
    pktSeqNo, message = rawData.split(DELIMITER)
    return pktSeqNo, message

def pktEncoder(pktSeqNo, message) :
    pkt = str(pktSeqNo) + DELIMITER + message
    return pkt.encode('utf-8')

def pingTestReport() :
    lostRatio = lostPing / sentPing
    print("\n[ 10 Ping Packets Result ]\n")
    print("Ping Sent : %d" % sentPing)
    print("Ping Received : %d" % recvPing)
    print("Ping Lost : %d" % lostPing)
    print("Lost Ratio : %.2f" % round(lostRatio, 2))
    print("minRTT : %d ms, maxRTT : %d ms, avgRTT : %d ms\n" % (minRTT, maxRTT, avgRTT))

def IPValidation(IPAddr) :
    IPs = IPAddr.split('.')

    for ip in IPs :
        if ip.isdecimal() == False or int(ip) < 0 or int(ip) > 255 :
            return False
    return True

def portValidation(portNumber) :
    if portNumber.isdecimal() == True and int(portNumber) >= 0 and int(portNumber) <= 65535 :
        return True
    else :
        return False

def timeoutTimeValidation(t) :
    if t.isdecimal() == True and int(t) >= 0 :
        return True
    else :
        return False

try :
    opts,args = getopt.getopt(sys.argv[1:], "c:p:w:")
except getopt.GetoptError as err :
    print(str(err))
    sys.exit(1)

for opt, arg in opts :
    if opt == '-c' :
        if IPValidation(arg) == True :
            serverIP = arg
        else :
            print("Invaild IP address for option -c.")
            sys.exit(1)
    elif opt == '-p' :
        if portValidation(arg) == True :
            serverPort = int(arg)
        else :
            print("Invalid Port number for option -p.")
            sys.exit(1)
    elif opt == '-w' :
        if timeoutTimeValidation(arg) == True :
            timeoutInterval = int(arg)
        else :
            print("Invalid timeout time for optino -w")
            sys.exit(1)



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
signal.signal(signal.SIGINT, signal_handler)
print("Ping test to <%s:%s>, Timeout time : %d" % (serverIP, serverPort, timeoutInterval))

for i in range(10) :
    try :
        pktSeqNo = str(i)

        startTime = now()
        sock.sendto(pktEncoder(pktSeqNo,message), (serverIP, serverPort))
        print ("\n%s %s sent" % (message, pktSeqNo))
        sentPing += 1
        sock.settimeout(timeoutInterval / 1000)

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
                remainTime = (timeoutInterval - elapsedTime) / 1000
                sock.settimeout(remainTime)
                continue

    except socket.timeout :
        print("PING %s timeout!" % pktSeqNo)
        lostPing += 1

pingTestReport()