import json
from datetime import datetime
from . import file_handler
from . import sso_util


def get_role_session_credentials(profile, role_arn=None):
    access_token = __get_access_token(profile)
    if role_arn is None:
        account_id = sso_util.get_account_id(access_token)
        role_name = sso_util.get_role_name(access_token, account_id)
        credentials = sso_util.get_role_credentials(
            access_token,
            account_id,
            role_name
        )
    else:
        account_role = __parse_role_arn(role_arn)
        credentials = sso_util.get_role_credentials(
            access_token,
            account_role['account_id'],
            account_role['role_name']
        )
    return credentials


def __get_access_token(profile):
    count = 0
    while True:
        try:
            access_token = file_handler.get_sso_access_token()
            sso_util.test_access_token(access_token)
            return access_token
        except:
            if count >= 1:
                raise Exception('Unable to retrieve SSO Access Token')
            else:
                count += 1
                sso_util.exec_login(profile)
                continue


def __parse_role_arn(role_arn):
    arn_parts = role_arn.split(':')
    return {
        'account_id': arn_parts[4],
        'role_name': arn_parts[5].lstrip('role/')
    }


def print_export_strings(cred):
    access_key_id = cred['accessKeyId']
    secret_access_key = cred['secretAccessKey']
    session_token = cred['sessionToken']
    print(f"export AWS_ACCESS_KEY_ID='{access_key_id}'")
    print(f"export AWS_SECRET_ACCESS_KEY='{secret_access_key}'")
    print(f"export AWS_SESSION_TOKEN='{session_token}'")


def store_session_credentials(profile=None):
    print('todo: store session credentials')
    if profile is None:
        # store creds in default
        pass
    else:
        # store credential process in profile
        # https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html
        pass


def print_credentials(cred):
    expiration_date = datetime.fromtimestamp(cred['expiration'] / 1e3)
    spec = {
        'Version': 1,
        'AccessKeyId': cred['accessKeyId'],
        'SecretAccessKey': cred['secretAccessKey'],
        'SessionToken': cred['sessionToken'],
        'Expiration': expiration_date.isoformat()
    }
    print(json.dumps(spec, separators=(',', ':')))
