import json
import configparser
from pathlib import Path
from . import helper


def get_sso_access_token(cache_dir=None):
    if cache_dir is None:
        cache_dir = '~/.aws/sso/cache/'
    keys = {'accessToken', 'expiresAt'}
    for file in __get_json_files(cache_dir):
        content = json.loads(__get_file_contents(file))
        if (content.keys() >= keys and helper.is_not_expired(content['expiresAt'])):
            return content['accessToken']


def __get_json_files(dir):
    p = Path(dir).expanduser()
    files = []
    if p.exists() and p.is_dir():
        for file in p.iterdir():
            if file.suffix == '.json':
                files.append(file)
    else:
        raise NotADirectoryError(f'Directory not found: {dir}')
    return files


def __get_file_contents(file_path):
    p = Path(file_path).expanduser()
    if p.exists() and p.is_file():
        return p.read_text()
    else:
        raise FileNotFoundError(f'File not found: {file_path}')


def get_credentials_config(file_path=None):
    file_path = helper.get_env_var('AWS_SHARED_CREDENTIALS_FILE', file_path)
    return __get_config(file_path)


def write_credentials_config(config, file_path=None):
    file_path = helper.get_env_var('AWS_SHARED_CREDENTIALS_FILE', file_path)
    __write_config(config, file_path)


def get_awsconfig_config(file_path=None):
    file_path = helper.get_env_var('AWS_CONFIG_FILE', file_path)
    return __get_config(file_path)


def write_awsconfig_config(config, file_path=None):
    file_path = helper.get_env_var('AWS_CONFIG_FILE', file_path)
    __write_config(config, file_path)


def __get_config(file_path):
    config = configparser.ConfigParser(default_section='default')
    p = Path(file_path).expanduser()
    if p.exists() and p.is_file():
        with p.open() as f:
            config.read_file(f)
    return config


def __write_config(config, file_path):
    p = Path(file_path).expanduser()
    with p.open(mode='w') as f:
        config.write(f)
