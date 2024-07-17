import struct
from . import protocol
import ipaddress

def search_frame():
    return serialize(command=protocol.Commands.SEARCH, module_mac=bytes.fromhex('0' * 12))

def get_frame(module_mac=None):
    return serialize(command=protocol.Commands.GET, module_mac=module_mac)
        
def deserialize_header(bytes_buffer):
    deserialize_format = "16sB6s6sB"
    comm_flag, command_header, ch9121_mac, pc_mac, data_area_len = struct.unpack(deserialize_format, bytes_buffer[:30])
    data = bytes_buffer[30 : 30 + data_area_len]
    return command_header, ch9121_mac, pc_mac, data_area_len, data

def serialize(command: protocol.Commands, module_mac=None, pc_mac=None, payload=None): 
    length = len(payload) if payload is not None else 0
    module_mac = module_mac if module_mac is not None else bytes.fromhex(12 * 'f')
    pc_mac = pc_mac if pc_mac is not None else bytes.fromhex(12 * '0')
    serialize_format = 'B6s6sB'
    if payload is None:
        payload = bytes.fromhex(protocol.payload_size * 2 * '0')
    elif len(payload) < protocol.payload_size:
        pad_amount = protocol.payload_size- len(payload)
        payload += bytes.fromhex(2 * pad_amount * '0')
    elif len(payload) > protocol.payload_size:
        raise ValueError('Message data section too long')    
    header = struct.pack(serialize_format, command.value, module_mac, pc_mac, length)

    message = protocol.preamble + header + payload
    return message

def deserialize_config(data_bytes):
    """
    struct __attribute__((__packed__)) DEVICEHW_CONFIG
    {
        UCHAR bDevType;                         /* device type, read-only*/
        UCHAR bAuxDevType;                      /* device subtype, read-only*/
        UCHAR bIndex;                           /* device serial number, read-only*/
        UCHAR bDevHardwareVer;                  /* device hardware version number, read-only*/
        UCHAR bDevSoftwareVer;                  /* device software version number, read-only*/
        UCHAR szModulename[21];                 /* user name is the same as CH9121 name*/
        UCHAR bDevMAC[6];                       /* CH9121 network MAC address */
        UCHAR bDevIP[4];                        /* CH9121 IP address */
        UCHAR bDevGWIP[4];                      /* CH9121 gateway IP */
        UCHAR bDevIPMask[4];                    /* CH9121 subnet mask */
        UCHAR bDhcpEnable;                      /* DHCP enable, whether to enable DHCP, 1: enable, 0: not enable*/
        USHORT breserved1;                      /* reserved but not yet enabled*/
        UCHAR breserved2[8];                    /* reserved but not yet enabled*/
        UCHAR breserved3;                       /* reserved but not yet enabled*/
        UCHAR breserved4[8];                    /* reserved but not yet enabled*/
        UCHAR breserved5;                       /* reserved but not yet enabled*/
        UCHAR bComcfgEn;                        /* serial port negotiation configuration flag 1: Enable 0: Disable */
        UCHAR breserved6[8];                    /* reserved but not yet enabled*/
    };
    """
    # deserialize DEVICEHW_CONFIG
    deserialization_format = 'BBBBB21s6s4s4s4sBBB8sB8sBB8s'
    device_hw_config = data_bytes[:74]
    dev_type, aux_dev_type, sn, hardware_ver, software_ver,\
    module_name, dev_mac, dev_ip, dev_gateway_ip, dev_ip_mask,\
    dhcp_enable, reserved_1, reserved_1a, reserved_2, reserved_3, reserved_4,\
    reserved_5, b_com_cfg_en, reserved_6 = struct.unpack(deserialization_format, device_hw_config)

    hw_config = {'Device type': dev_type,
                 'Device subtype': aux_dev_type,
                 'Serial number': sn,
                 'Hardware version': hardware_ver,
                 'Software version': software_ver,
                 'Module name' : module_name.decode().rstrip('\x00'),
                 'Device MAC': dev_mac.hex(),
                 'Device IP': str(ipaddress.IPv4Address(dev_ip)),
                 'Device Gateway IP': str(ipaddress.IPv4Address(dev_gateway_ip)),
                 'Device IP Mask': str(ipaddress.IPv4Address(dev_ip_mask)),
                 'DHCP Enable': bool(dhcp_enable),
                 'Serial port negotiation configuration enable': bool(b_com_cfg_en)
                 }
    
    # deserialize DEVICEPORT_CONFIG
    # note: ULONG is 4 bytes wide
    deserialization_format = "BBBBH4sHiBBBBiiBBB20s14s"
    device_port_1_config_bytes = data_bytes[74: 74 + 65]
    device_port_2_config_bytes = data_bytes[74 + 65: 74 + 65 * 2]
    """
    struct __attribute__((__packed__)) DEVICEPORT_CONFIG
    {
        UCHAR bIndex;                           /* sub-device serial number, read-only */
        UCHAR bPortEn;                          /* port enable flag 1: Enable; 0: Disable*/
        UCHAR bNetMode;                         /* network working mode: 0: TCP SERVER; 1: TCP CLENT; 2: UDP SERVER 3: UDP CLIENT; */
        UCHAR bRandSportFlag;                   /* random local port number in TCP client mode, 1: random 0: not random*/
        USHORT wNetPort;                        /* local port number*/  
        UCHAR bDesIP[4];                        /* destination IP address */
        //10
        USHORT wDesPort;                        /* destination port number*/
        ULONG dBaudRate;                        /* serial port baud rate: 300---921600bps */
        UCHAR bDataSize;                        /* serial port data bits: 5---8 bits*/  
        UCHAR bStopBits;                        /* serial port stop bit: 0 means 1 stop bit; 1 means 1.5 stop bits; 2 means 2 stop bits*/  
        UCHAR bParity;                          /* serial port parity bit: 4 means no parity, 0 means odd parity; 1 means even parity; 2 means mark bit (MARK, set to 1); 3 means space bit (SPACE, clear to 0); */    
        UCHAR bPHYChangeHandle;                 /* PHY disconnected, Socket action, 1: close Socket 0: no action*/
        // 20
        ULONG dRxPktlength;                     /* serial port RX data packet length, maximum 1024 */
        ULONG dRxPktTimeout;                    /* maximum waiting time for serial port RX data package forwarding, unit: 10ms, 0 means turning off the timeout function*/
        UCHAR bResv;                            /* reserved not enabled*/  
        UCHAR bResetCtrl;                       /* serial port reset operation: 0 means do not clear the serial port data buffer; 1 means clear the serial port data buffer when connected */  
        // 30
        UCHAR bDNSFlag;                         /* domain name function enable flag, 1: enable 0: disable */
        UCHAR szDomainname[20];                 /* In TCP client mode, destination address, domain name*/
        UCHAR breserved[14];                    /* reserved */
        // 65
    };
    """
    subdev_serial, port_en, netmode, random_local_port, local_port_number, dest_ip, dest_port,\
        baud, data_size, stop_bits, parity, phy_handle, rx_packet_length, rx_timeout, reserved_1, reset_ctl,\
        dns_flag, domain_name, reserved = struct.unpack(deserialization_format, device_port_1_config_bytes)
    port_1_cfg = {
        'Port subdevice serial number': subdev_serial,
        'Port Enable': bool(port_en),
        'Netmode': netmode,
        'Random local port enable': bool(random_local_port),
        'Local port number': local_port_number,
        'Destination IP': str(ipaddress.IPv4Address(dest_ip)),
        'Destination port': dest_port,
        'Baudrate': baud,
        'Data size': data_size,
        'Stop bits': stop_bits,
        'Parity': parity,
        'PHY Change Handle Enable': bool(phy_handle),
        'RX Packet Max Length': rx_packet_length,
        'RX Timeout': rx_timeout,
        'Clear RX data buffer on connection enable': bool(reset_ctl),
        'DNS Enable': bool(dns_flag),
        'Domain name': domain_name.decode().rstrip('\x00')
    }
    subdev_serial, port_en, netmode, random_local_port, local_port_number, dest_ip, dest_port,\
        baud, data_size, stop_bits, parity, phy_handle, rx_packet_length, rx_timeout, reserved_1, reset_ctl,\
        dns_flag, domain_name, reserved= struct.unpack(deserialization_format, device_port_2_config_bytes)

    port_2_cfg = {
        'Port subdevice serial number': subdev_serial,
        'Port Enable': bool(port_en),
        'Netmode': netmode,
        'Random local port enable': bool(random_local_port),
        'Local port number': local_port_number,
        'Destination IP': str(ipaddress.IPv4Address(dest_ip)),
        'Destination port': dest_port,
        'Baudrate': baud,
        'Data size': data_size,
        'Stop bits': stop_bits,
        'Parity': parity,
        'PHY Change Handle Enable': bool(phy_handle),
        'RX Packet Max Length': rx_packet_length,
        'RX Timeout': rx_timeout,
        'Clear RX data buffer on connection enable': bool(reset_ctl),
        'DNS Enable': bool(dns_flag),
        'Domain name': domain_name.decode().rstrip('\x00')
    }
    config = {'HW Config': hw_config,
              'Port 1 Config': port_1_cfg,
              'Port 2 Config': port_2_cfg}
    return config