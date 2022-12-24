import os 

WORKING_PATH = os.path.abspath(os.path.dirname(__file__))
DEFAULT_CONFIG_PATH = os.path.join(WORKING_PATH, "config.txt")
BOT_DATA_PATH = os.path.join(os.path.join(WORKING_PATH, "bot_data"), "bot.dat")


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


def file_exists(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False

def create_file(file_path):
    with open(file_path, "w"):
        pass

def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)
