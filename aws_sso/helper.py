from os import environ
from datetime import datetime, timezone
from dateutil import parser


def get_role_arn(account_id, role_name):
    return f'arn:aws:iam::{account_id}:role/{role_name}'


def parse_role_arn(role_arn):
    arn_parts = role_arn.split(':')
    return {
        'account_id': arn_parts[4],
        'role_name': arn_parts[5].lstrip('role/')
    }


def int_to_datetime(int_datetime):
    return datetime.fromtimestamp(int_datetime / 1e3, tz=timezone.utc)


def is_not_expired(expires_at):
    expiration_date = parser.parse(expires_at)
    return expiration_date > datetime.now(timezone.utc)


def minutes_from_now(expires_at):
    expiration_date = parser.parse(expires_at)
    return int((expiration_date - datetime.now(timezone.utc))
               .total_seconds() / 60)


def get_env_var(env_var):
    if env_var in environ:
        val = environ[env_var]
    else:
        if env_var == 'AWS_CONFIG_FILE':
            val = '~/.aws/config'
        if env_var == 'AWS_SHARED_CREDENTIALS_FILE':
            val = '~/.aws/credentials'
    return val
