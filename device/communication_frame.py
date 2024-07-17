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
    dev_type, aux_dev_type, sn, hardware_ver, software_ver,\
    module_name, dev_mac, dev_ip, dev_gateway_ip, dev_ip_mask,\
    dhcp_enable, reserved_1, reserved_1a, reserved_2, reserved_3, reserved_4,\
    reserved_5, b_com_cfg_en, reserved_6 = struct.unpack(deserialization_format, data_bytes[:74])

    # print(dev_type, aux_dev_type, sn, hardware_ver, software_ver,\
    # module_name, dev_mac, dev_ip, dev_gateway_ip, dev_ip_mask,\
    # dhcp_enable, reserved_1, reserved_1a, reserved_2, reserved_3, reserved_4,\
    # reserved_5, b_com_cfg_en, reserved_6)

    print(ipaddress.IPv4Address(dev_ip))