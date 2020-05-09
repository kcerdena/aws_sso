import pytest
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
    assert token == None


def test_get_sso_access_token_non_token(tmp_path):
    f = tmp_path / "non_token_file.json"
    f.write_text(non_token_file)
    token = file_handler.get_sso_access_token(tmp_path)
    assert token == None


def today_with_delta(days_delta):
    format = '%Y-%m-%dT%H:%M:%S%Z'
    test_date = datetime.now(timezone.utc) + timedelta(days=days_delta)
    return test_date.strftime(format)


expired_token_file = f'{{"accessToken": "ThisTokenIsExpired", "expiresAt": "{today_with_delta(-1)}"}}'
valid_token_file = f'{{"accessToken": "ThisTokenIsValid", "expiresAt": "{today_with_delta(1)}"}}'
non_token_file = f'{{"arbitraryKey": "arbitraryValue", "expiresAt": "{today_with_delta(1)}"}}'
