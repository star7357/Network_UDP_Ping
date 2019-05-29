# client_skel.py
import socket

DELIMITER = '\n'

server_ip = 'nsl2.cau.ac.kr'
server_port = 34367

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def pktDecoder(data) :
    rawData = data.decode('utf-8')
    pktSeqNo, message = rawData.split(DELIMITER)
    return pktSeqNo, message

def pktEncoder(pktSeqNo, message) :
    pkt = str(pktSeqNo) + DELIMITER + message
    return pkt.encode('utf-8')

message = "Ping"

for i in range(10) :
    pktSeqNo = i

    sock.sendto(pktEncoder(pktSeqNo,message), (server_ip, server_port))
    print ("Client: send \"" + message + "\", pktNo : " + str(pktSeqNo))

    data, addr = sock.recvfrom(1024)
    a,b = pktDecoder(data)
    print ("Client: recv \"" + b + "\", pktNo : " + str(a))
