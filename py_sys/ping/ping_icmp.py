# coding=utf-8

import os
import socket
import struct
import select
import time

ICMP_ECHO_RESPONSE = 0
ICMP_ECHO_REQUEST = 8

class PingICMP():
    '''
    PingICMP reference Linux implemented and RFC 792
    '''
    
    def __init__(self):
        pass
 
    def __checksum(self, source_string):
        _sum = 0
        countTo = (len(source_string) / 2) * 2
        count = 0
        while count < countTo:
            thisVal = ord(source_string[count + 1]) * 256 + ord(source_string[count])
            _sum = _sum + thisVal
            _sum = _sum & 0xffffffff
            count = count + 2
     
        if countTo < len(source_string):
            _sum = _sum + ord(source_string[len(source_string) - 1])
            _sum = _sum & 0xffffffff 
     
        _sum = (_sum >> 16) + (_sum & 0xffff)
        _sum = _sum + (_sum >> 16)
        answer = ~_sum
        answer = answer & 0xffff
     
        answer = answer >> 8 | (answer << 8 & 0xff00)
     
        return answer
     
     
    def __receive_icmp_response(self, icmp_socket, packet_id, timeout):

        time_left = timeout
        
        while True:
            start_time = time.time()
            select_ready = select.select([icmp_socket], [], [], time_left)
            select_interval = (time.time() - start_time)
            if select_ready[0] == []:
                return
     
            time_received = time.time()
            packet, _ = icmp_socket.recvfrom(1024)
            icmp_header = packet[20 : 28]
            rep_type, _, _, pkt_id, _ = struct.unpack(
                'bbHHh', icmp_header
            )
            if rep_type is ICMP_ECHO_RESPONSE and pkt_id == packet_id:
                packet_bytes = struct.calcsize('d')
                time_sent = struct.unpack('d', packet[28 : 28 + packet_bytes])[0]
                return time_received - time_sent
     
            time_left = time_left - select_interval
            if time_left <= 0:
                return
     
     
    def __send_icmp_request(self, icmp_socket, dest_addr, packet_id, sequence):
        
        # ICMP Header :
        # -------------------------------------------------------------------
        # | type(8) | code(8) | checksum(16) | packet_id(16) | sequence(16) |
        # -------------------------------------------------------------------
        #
        packet_checksum = 0
     
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, packet_checksum, packet_id, sequence)
        packet_bytes = struct.calcsize('d')
        
        data = (128 - packet_bytes) * '0'
        data = struct.pack('d', time.time()) + data
     
        packet_checksum = self.__checksum(header + data)
     
        header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(packet_checksum), packet_id, sequence)
        packet = header + data
        icmp_socket.sendto(packet, (dest_addr, 1))
     
     
    def ping_once(self, dest_addr, timeout, sequence):
        icmp = socket.getprotobyname('icmp')
        
        try:
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error, (errno, msg):
            if errno == 1:
                msg = '%s : Just root can send ICMP Message' % msg
                raise socket.error(msg)
            raise
     
        packet_id = os.getpid() & 0xFFFF
     
        self.__send_icmp_request(icmp_socket, dest_addr, packet_id, sequence)
        delay = self.__receive_icmp_response(icmp_socket, packet_id, timeout)
     
        icmp_socket.close()
        return delay
     
     
    def ping(self, host_name, timeout = 10, count = 5):
        ping_result_list = []
        
        try:
            dest_addr = socket.gethostbyname(host_name)
        except socket.gaierror, e:
            raise IOError('%s is not right hostname or ip' % host_name)
            
        for i in xrange(count):
            ping_result = {'host_name' : host_name, 'dest_addr' : dest_addr}
            try:
                delay = self.ping_once(dest_addr, timeout, i)
                if delay is not None:
                    ping_result['result'] = 'success'
                    ping_result['delay'] = delay * 1000
                else:
                    ping_result['result'] = 'timeout'
            except socket.gaierror, e:
                ping_result['result'] = 'exception'
                ping_result['message'] = e
            
            ping_result_list.append(ping_result)
            
        return ping_result_list

