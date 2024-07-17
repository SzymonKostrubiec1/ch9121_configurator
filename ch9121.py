from device import device
from device import store_config

module = device.CH9121(interface='enxc84d4425916c')
print("Search")
module_macs = module.search()
print("get config")
config = module.get_config(module_mac=module_macs[0])
print(config)
store_config.config_save(config, 'config-saved.yaml')

# TODO: addressing all devices doesn't work
# module.get_config(module_mac=None)