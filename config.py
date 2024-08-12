import os
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # Create a parser
    parser = ConfigParser()
    # Get the absolute path to the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Join the path to the config file
    config_path = os.path.join(current_dir, filename)
    # Read config file
    parser.read(config_path)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


config()
