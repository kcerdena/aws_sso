import json
from . import file_handler
from . import sso_util
from . import helper
from botocore.exceptions import ParamValidationError, ClientError


def get_role_session_credentials(sso_profile, role_arn=None):
    access_token = __get_access_token(sso_profile)
    if role_arn is None:
        account_id = sso_util.get_account_id(access_token)
        role_name = sso_util.get_role_name(access_token, account_id)
        role_arn = helper.get_role_arn(account_id, role_name)
    return sso_util.get_role_credentials(
        access_token,
        role_arn
    )


def __get_access_token(sso_profile):
    count = 0
    while True:
        try:
            access_token = file_handler.get_sso_access_token()
            # Verify access token is still valid
            sso_util.get_account_list(access_token)
            return access_token
        except (ParamValidationError, ClientError):
            if count >= 1:
                raise RuntimeError('Unable to retrieve SSO Access Token')
            else:
                count += 1
                sso_util.exec_login(sso_profile)
                continue


def store_default_role_session_credentials(cred):
    config = __get_default_credentials_config(cred)
    file_handler.write_credentials_config(config)


def __get_default_credentials_config(cred):
    config = file_handler.get_credentials_config()
    config['default']['aws_access_key_id'] = cred['accessKeyId']
    config['default']['aws_secret_access_key'] = cred['secretAccessKey']
    config['default']['aws_session_token'] = cred['sessionToken']
    return config


def print_export_strings(cred):
    access_key_id = cred['accessKeyId']
    secret_access_key = cred['secretAccessKey']
    session_token = cred['sessionToken']
    print(f"export AWS_ACCESS_KEY_ID='{access_key_id}'")
    print(f"export AWS_SECRET_ACCESS_KEY='{secret_access_key}'")
    print(f"export AWS_SESSION_TOKEN='{session_token}'")


def print_credentials(cred):
    expiration_date = helper.int_to_datetime(cred['expiration'])
    spec = {
        'Version': 1,
        'AccessKeyId': cred['accessKeyId'],
        'SecretAccessKey': cred['secretAccessKey'],
        'SessionToken': cred['sessionToken'],
        'Expiration': expiration_date.isoformat()
    }
    print(json.dumps(spec, separators=(',', ':')))
