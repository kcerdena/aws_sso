import json
import configparser
from datetime import datetime, timezone
from dateutil import parser
from pathlib import Path


def get_sso_access_token(cache_dir='~/.aws/sso/cache/'):
    keys = {'accessToken', 'expiresAt'}
    for file in __get_json_files(cache_dir):
        content = json.loads(__get_file_contents(file))
        if content.keys() >= keys and __is_not_expired(content['expiresAt']):
            return content['accessToken']


def __get_json_files(dir):
    p = Path(dir).expanduser()
    files = []
    if p.exists() and p.is_dir():
        for file in p.iterdir():
            if file.suffix == '.json':
                files.append(file)
    else:
        raise Exception(f'Directory not found: {dir}')
    return files


def __get_file_contents(file_path):
    p = Path(file_path).expanduser()
    if p.exists() and p.is_file():
        return p.read_text()
    else:
        raise Exception(f'File not found: {file_path}')


def __is_not_expired(expires_at):
    expiration_date = parser.parse(expires_at)
    return expiration_date > datetime.now(timezone.utc)


def get_credentials_config(credentials_file='~/.aws/credentials'):
    config = configparser.ConfigParser(default_section='default')
    p = Path(credentials_file).expanduser()
    if p.exists() and p.is_file():
        with p.open() as f:
            config.read_file(f)
    return config


def write_credentials_config(config, credentials_file='~/.aws/credentials'):
    p = Path(credentials_file).expanduser()
    with p.open(mode='w') as f:
        config.write(f)