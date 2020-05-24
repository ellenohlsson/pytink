import yaml


def _parse_config(config_file):

    with open(config_file, 'r') as cf:
        try:
            config = yaml.safe_load(cf)
            return config
        except yaml.YAMLError as e:
            print(e)


def load_config(config_file):
    return _parse_config(config_file)
