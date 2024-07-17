from enum import Enum

"""
typedef struct NET_COMM {
	unsigned char flag[16];		                          // Constant value of b'CH9121_CFG_FLAG\x00'
	unsigned char cmd;			                          // Command
	unsigned char id[6];		                          // Addressed module ID. 0xffffff to address all modules
	unsigned char cfg_mac[6];	                          // Device MAC configuration
	unsigned char len;			                          //
	unsigned char data[NET_MODULE_DATA_LENGTH];	          //
}net_comm,*pnet_comm;

typedef struct _Mod_MacIP{
	unsigned char mod_ip[4];
	unsigned char mod_mac[6];
	unsigned char mod_name[21];
	unsigned char mod_ver;
}Mod_MacIP,pMod_MacIP; 

typedef struct _DEVICEHW_CONFIG
{
	UCHAR  bDevType;            // device type
	UCHAR  bAuxDevType;			// device subtype
	UCHAR  bIndex;			    // serial number 
	UCHAR  bDevHardwareVer;		// hardware revision
	UCHAR  bDevSoftwareVer;		// software version
	UCHAR  szModulename[21];    // device name 
	UCHAR  bDevMAC[ 6 ];		// device mac
	UCHAR  bDevIP[ 4 ];    		// device ip	
	UCHAR  bDevGWIP[ 4 ];    	// device gateway ip 
	UCHAR  bDevIPMask[ 4 ];    	// device subnet mask	
	UCHAR  bDhcpEnable;		    // DHCP enable
	USHORT wWebPort;			// Web address? Posibly port name
	UCHAR  szUsername[8];		// Username, equal to device name	
	UCHAR  bPassWordEn;			// Password enable	
	UCHAR  szPassWord[8];	    // Password
	UCHAR  bUpdateFlag;			//Update enable
	UCHAR  bComcfgEn;			// Uart config	
	UCHAR  breserved[8];				
}DeviceHWConfigS,*pDeviceHWConfigS;

typedef struct _DEVICEPORT_CONFIG
{
	UCHAR  bIndex;				// Uart index / number	
	UCHAR  bPortEn;				// Port enable	
	UCHAR  bNetMode;			// Net settings: 0 - TCP server 1 - TCP client 2 - UDP server 3 - UDP client	
	UCHAR  bRandSportFlag;		// Random local port in TCP client mode enable
	USHORT wNetPort;			// Port number
	UCHAR  bDesIP[ 4 ];    	    // Client mode destination IP
	USHORT wDesPort;			// Client mode destination port	
	ULONG  dBaudRate;			// UART Baudrate 300 - 921600 bps	
	UCHAR  bDataSize;			// Data byte size	
	UCHAR  bStopBits;			// Stop bits	
	UCHAR  bParity;				// Parity	
	UCHAR  bPHYChangeHandle;	// Buffer data while ETH disconnected enable?
	ULONG  dRxPktlength;		// UART RX max buffer size	
	ULONG  dRxPktTimeout;		// Max UART buffer delay, units of 10ms, 0 - no buffering	
	UCHAR  bReConnectCnt;		// Max connection retries to TCP server in TCP client mode
	UCHAR  bResetCtrl;			// Clear uart buffer on connection reset enable
	UCHAR  bDNSFlag;			// DNS Enable
	UCHAR  szDomainname[20];    // Domain name
	UCHAR  bDNSHostIP[4];		// DNS provider IP
	USHORT wDNSHostPort;		// DNS provider port
	UCHAR  breserved[8];			
}DevicePortConfigS,*pDevicePortConfigS;

typedef struct _NET_DEVICE_CONFIG
{   
	DeviceHWConfigS     HWCfg;			     
	DevicePortConfigS   PortCfg[2];          
}NetDeviceConfigS,*pNetDeviceConfigS;

"""
message_size = 285
header_size = 30
payload_size = message_size - header_size
preamble = bytes.fromhex('43 48 39 31 32 31 5F 43 46 47 5F 46 4C 41 47 00'.replace(' ', ''))

class Commands(Enum):
    SET = 0x01
    GET = 0x02
    RESET_TO_FACTORY = 0x03
    SEARCH = 0x04

class Ack(Enum):
    ACK_SET = 0x81
    ACK_GET = 0x82
    ACK_RESET_TO_FACTORY = 0x83
    ACK_SEARCH = 0x84
    
class NAck(Enum):
    NACK_SEARCH = 0xc0
    NACK_SET = 0xc1
    NACK_GET = 0xc2