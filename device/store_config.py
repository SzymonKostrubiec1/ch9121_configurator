import yaml

def config_save(config, filename):
    with open(filename, 'w') as file:
        yaml.dump(config, file)