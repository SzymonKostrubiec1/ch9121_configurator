import argparse

from device import device
from device import store_config

parser = argparse.ArgumentParser(prog='CH9121 Programmer', description=
                                 'Multiple actions may be specified and performed,'
                                 ' in the order specified below.')
parser.add_argument('-s', '--search', default=False, action='store_true', help=
                    'Search for device')
parser.add_argument('-g', '--get', default=False, action='store_true',
                    help='Download device configuration. '
                    'Save to file specified by --output-file')
parser.add_argument('--set', default=False, action='store_true',
                    help='Program device with specified configuration. '
                    'Specify --input-file')
parser.add_argument('-r', '--reset', default=False, action='store_true',
                    help='Restore device to factory settings')
parser.add_argument('-if', '--input-file', default=None,
                     help='Configuration input file')
parser.add_argument('-of', '--output-file', default='config-saved.yaml',
                    help='Configuration output file. Defaults to config-saved.yaml')
parser.add_argument('-i', '--interface', default='enxc84d4425916c',
                    help='Specify network interface to use')
parser.add_argument('-m', '--mac', default=None, help='Target MAC. If unspecfied, '
                    'the program will target the only device on network or stop, if there '
                    'is more than one. Hexadecimal format with no separators')
args = parser.parse_args()

module = device.CH9121(args.interface)

target_mac = args.mac

if args.search:
    print("Searching")
    module_macs = module.search()

    if module_macs:
        print(f'Found {len(module_macs)} devices:')
        for i in range(len(module_macs)):
            print(f'{i}. {module_macs[i]}')

    else:
        print('No devices found')

    if len(module_macs) == 1 and args.mac is None:
        target_mac = module_macs[0]

if args.get:
    if target_mac is None:
        print('No target MAC specified and no available devices found.')
        exit(1)
    print(f'Asking {target_mac} for its configuration')
    config = module.get_config(module_mac=target_mac)
    store_config.config_save(config, args.output_file)
if args.set:
    if target_mac is None:
        print('No target MAC specified and no available devices found.')
        exit(1)
    if args.output_file is None:
        print('Set was specified but no configuration file was selected')
        exit(1)
    print(f'Sending configuration specified in {args.output_file} to {target_mac}')
    config = store_config.config_load(args.output_file)
    module.set_config(config, module_mac=target_mac)

if args.reset:
    if target_mac is None:
        print('No target MAC specified and no available devices found.')
        exit(1)
    print(f'Asking {target_mac} to revert to factory settings.')
    module.reset_to_factory_settings(module_mac=target_mac)
