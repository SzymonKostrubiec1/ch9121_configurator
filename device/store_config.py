import yaml

def config_save(config, filename):
    with open(filename, 'w') as file:
        yaml.dump(config, file)

def config_load(filename):
    with open('device/default_config.yaml', 'r') as f:
        default_config = yaml.load(f, yaml.loader.FullLoader)

    with open(filename, 'r') as f:
        new_config = yaml.load(f, yaml.loader.FullLoader)
    # if an entry is in both dictionaries, the new_config is choosen

    # TODO: check if protecting against overwriting read only data is neccessary
    # TODO: input sanitization

    config = default_config

    for config_type in new_config.keys():
        for item in new_config[config_type].keys():
            try:
                config[config_type][item] = new_config[config_type][item]
            except:
                raise ValueError('Specified parameter is not allowed')

    return default_config # FIXME

