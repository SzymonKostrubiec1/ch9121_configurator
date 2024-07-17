import socket
import time
import threading
from . import protocol
from . import communication_frame
from . import store_config

broadcast_ip = "192.168.1.255"
send_port = 50000
receive_port = 60000

this_device_mac = "50 54 7b b5 0e 56"
SO_BINDTODEVICE = 25

def send_data(data, broadcast_ip, port):
    socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    socket_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    time.sleep(0.2)
    socket_send.sendto(data, (broadcast_ip, port))

class CH9121:

    def __init__(self, interface=None, broadcast_ip=broadcast_ip, 
                 send_port=send_port, receive_port=receive_port):
        self.socket_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.socket_receive.bind(('', receive_port))
        if interface is not None:
            self.socket_receive.setsockopt(socket.SOL_SOCKET, SO_BINDTODEVICE, str(interface).encode())
        self.target_ip = broadcast_ip
        self.target_port = send_port
        self.search_max_devices = 5

    def search(self):
        search_packet = communication_frame.search_frame()
        t = threading.Thread(target=send_data, args=(search_packet, self.target_ip, self.target_port))
        t.start()
        self.socket_receive.settimeout(3)
        try:
            response = self.socket_receive.recv(protocol.message_size * self.search_max_devices)
        except TimeoutError:
            response = None
        responses_count = int(len(response) / protocol.message_size)
        device_macs = []
        for i in range(responses_count):
            command_header, ch9121_mac, pc_mac, data_area_len, data = communication_frame.deserialize_header(
                response[i * protocol.message_size : (i + 1) * protocol.message_size])
            assert command_header == protocol.Ack.ACK_SEARCH.value
            device_macs.append(ch9121_mac)
        print(f'Found {responses_count} devices')
        for i in range(responses_count):
            print(device_macs[i].hex())
        t.join()
        return device_macs

    def get_config(self, module_mac=None):
        get_packet = communication_frame.get_frame(module_mac=module_mac)
        t = threading.Thread(target=send_data, args=(get_packet, self.target_ip, self.target_port))
        t.start()
        # TODO: handle possibility of communicating with many devices
        try:
            response = self.socket_receive.recv(285)
        except TimeoutError:
            print("Timed out waiting for a get response packet. Terminating")
            exit(1)
        command_header, ch9121_mac, pc_mac, data_area_len, data = communication_frame.deserialize_header(
                response)
        assert command_header == protocol.Ack.ACK_GET.value
        config = communication_frame.deserialize_config(data)
        t.join()

        return config

    def set_config(self):
        set_packet = """43 48 39 31 32 31 5F 43 46 47 5F 46 4C 41 47 00 01 ff ff ff ff ff ff F4 8E 38
        8B FC 9F CC 21 21 01 02 03 43 48 39 31 32 31 20 00 00 00 00 00 00 00 00 00 00
        00 00 00 00 02 03 04 05 06 07 C0 A8 01 14 C0 A8 01 01 FF FF FF 00 00 50 00 00
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF 00 FF FF FF FF FF FF FF FF
        00 00 02 01 B8 0B C0 A8 01 64 D0 07 80 25 00 00 08 01 04 01 00 04 00 00 00 00
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 FF
        FF FF FF FF FF FF FF FF FF FF FF FF FF 01 01 01 00 D0 07 C0 A8 01 0A E8 03 00
        C2 01 00 08 01 04 01 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF FF FF
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"""

        set_packet = set_packet.replace(' ', '').replace('\n', '')
        set_packet = bytes.fromhex(set_packet)
        t = threading.Thread(target=send_data, args=(set_packet, self.target_ip, self.target_port))
        t.start()
        response = self.socket_receive.recv(285)
        print(response)
        t.join()