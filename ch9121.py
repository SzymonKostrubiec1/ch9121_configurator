from device import device

module = device.CH9121(interface='enxc84d4425916c')
print("Search")
module_macs = module.search()
print("get config")
module.get_config(module_mac=module_macs[0])
# TODO: addressing all devices doesn't work
# module.get_config(module_mac=None)