from device import device
from device import store_config

module = device.CH9121(interface='enxc84d4425916c')
print("Search")
module_macs = module.search()
print("get config")
if len(module_macs) == 0:
    print('Could not find any devices')
    exit(1)
config = module.get_config(module_mac=module_macs[0])
store_config.config_save(config, 'config-saved.yaml')

config = store_config.config_load('config.yaml')
module.set_config(config, module_mac=module_macs[0])

# TODO: addressing all devices doesn't work
# module.get_config(module_mac=None)