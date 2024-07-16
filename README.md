# CH9121 configurator

Mini python program to set & get CH9121 chip parameters

## FAQ

CH9121 receives configuration on broadcast address on port 50000 and
sends replies to broadcast address to port 60000.

## Quick start

How to use this program. There are 2 options. Set and get configuration.

### List devices

`python3 sch9121.py -i eth0 -l`

Lists CH9121 all devices in network.

### Get parameters

`python3 ch9121.py -i -g`

It will print configuration to STDOUT in yaml format.

**Note** Store config to file:

`python3 sch9121.py -i eth0 -s config.yml > config.yml`

### Set parameters

`python3 sch9121.py -i eth0 -s config.yml`

## Config yaml

### Network section

```yaml

network_interface:
  type: dhcp
```

or

```yaml

network_interface:
  type: static
    ip: "192.168.1.17/24"
    gw: "192.168.1.1"
```

### UART

```yaml

uart0:
  connection: "TCP_SERVER"
    port: 2000
    # optional other thins in other types of connection
  serial_params:
    baudrate: 115200
    data_bits: 8
    stop_bits: 2
    parity: null 
  lost_connection_disconnect: false
  packet_length: 0
  packet_timeout: 0
  clear_buff_on_reconnect: true
```

## Which parameters are optional?
