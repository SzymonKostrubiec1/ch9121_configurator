import yaml

def config_save(config, filename):
    with open(filename, 'w') as file:
        yaml.dump(config, file)

def config_load(filename):

    with open(filename, 'r') as f:
        config = yaml.load(f, yaml.loader.FullLoader)

    return config


