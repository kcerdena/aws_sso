import configparser
from datetime import datetime, timezone, timedelta
from aws_sso import file_handler


def test_get_sso_access_token_valid(tmp_path):
    f = tmp_path / "valid_token_file.json"
    f.write_text(valid_token_file)
    token = file_handler.get_sso_access_token(tmp_path)
    assert token == 'ThisTokenIsValid'


def test_get_sso_access_token_expired(tmp_path):
    f = tmp_path / "expired_token_file.json"
    f.write_text(expired_token_file)
    token = file_handler.get_sso_access_token(tmp_path)
    assert token is None


def test_get_sso_access_token_non_token(tmp_path):
    f = tmp_path / "non_token_file.json"
    f.write_text(non_token_file)
    token = file_handler.get_sso_access_token(tmp_path)
    assert token is None


def test_get_credentials_config_empty(tmp_path):
    f = tmp_path / "credentials"
    config_file = file_handler.get_credentials_config(f)
    assert isinstance(config_file, configparser.ConfigParser)
    assert 1 == len(config_file.items())


def test_read_write_credentials_config(tmp_path):
    f = tmp_path / "credentials"
    f.write_text("[default]\nkey5 = value3\n\n[section1]\nkey1 = value1\n\n")
    config_file = file_handler.get_credentials_config(f)
    assert config_file.defaults()['key5'] == 'value3'
    assert config_file['section1']['key1'] == 'value1'
    config_file['section1']['key2'] = 'value2'
    file_handler.write_credentials_config(config_file, f)
    content = f.read_text()
    assert 'key2 = value2' in content


def today_with_delta(days_delta):
    format = '%Y-%m-%dT%H:%M:%S%Z'
    test_date = datetime.now(timezone.utc) + timedelta(days=days_delta)
    return test_date.strftime(format)


expired_token_file = f'{{"accessToken": "ThisTokenIsExpired", "expiresAt": "{today_with_delta(-1)}"}}'
valid_token_file = f'{{"accessToken": "ThisTokenIsValid", "expiresAt": "{today_with_delta(1)}"}}'
non_token_file = f'{{"arbitraryKey": "arbitraryValue", "expiresAt": "{today_with_delta(1)}"}}'
