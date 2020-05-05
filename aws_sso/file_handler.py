import configparser
from pathlib import Path


def get_file_contents(file_path):
    p = Path(file_path).expanduser()
    if p.exists() and p.is_file():
        return p.read_text()
    else:
        raise Exception('File not found')


def get_config(file_path):
    file_text = get_file_contents(file_path)
    cfg = configparser.ConfigParser()
    return cfg.read_string(file_text)

