from netifaces import ifaddresses, AF_INET

def get_broadcast_address(interface: str):
    try:
        return ifaddresses(interface)[AF_INET][0]['broadcast']
    except:
        print('Automatic broadcast lookup failed. Is the interface specified correctly?')
        exit(1)