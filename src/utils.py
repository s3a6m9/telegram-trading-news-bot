import os 

WORKING_PATH = os.path.abspath(os.path.dirname(__file__))
DEFAULT_CONFIG_PATH = os.path.join(WORKING_PATH, "config.txt")


def parse_config(config_path):
    """ Passes the contents of the config file in a dictionary format"""
    config_variables = {}
    with open(config_path, "r") as config_file:
        for line in config_file.readlines():
            if line.startswith("#") or line == "\n" or line == "":
                continue
            line = line.split("=")
            config_variables[line[0].strip().lower()] = line[1].strip()
    return config_variables
