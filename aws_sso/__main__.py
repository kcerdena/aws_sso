import argparse
import re
from . import credentials
from . import helper


def main(args):
    cred = credentials.get_role_session_credentials(
        args['profile'], args['rolearn']
    )
    account_id = helper.parse_role_arn(cred['role_arn'])['account_id']
    role_name = helper.parse_role_arn(cred['role_arn'])['role_name']
    expiration = helper.int_to_datetime(cred["expiration"]).isoformat()
    x_minutes = helper.minutes_from_now(expiration)
    credentials_file_path = helper.get_env_var('AWS_SHARED_CREDENTIALS_FILE')

    if args['external_source']:
        credentials.print_credentials(cred)
    else:
        if not args['no_store_creds']:
            credentials.store_default_role_session_credentials(cred)
            print(f'Temporary credentials added to {credentials_file_path}')
            print(f'Account: {account_id}')
            print(f'Role:    {role_name}')
            print(f'Expires: {expiration} ({x_minutes}m)')
        if args['env_vars']:
            credentials.print_export_strings(cred)


def validate_input(arg, input):
    if arg == 'rolearn' and input is None:
        match = True
    else:
        if arg == 'profile':
            pattern = r"^[\w\-\.]+$"
        if arg == 'rolearn':
            pattern = r"^arn\:aws\:iam\:\:\d{12}\:role/[\w+=,.@-]+$"
        match = re.match(pattern, str(input))
    return bool(match)


if __name__ == '__main__':
    description = ''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', '--profile', required=True,
                        help='Named profile for AWS SSO login')
    parser.add_argument('-r', '--rolearn',
                        help='RoleArn for session credentials')
    parser.add_argument('-ns', '--no-store-creds', action='store_true',
                        help='Disable output of session credential to AWS_SHARED_CREDENTIALS_FILE')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-env', '--env_vars', action='store_true',
                       help='Output session credential environment variable export strings')
    group.add_argument('-ext', '--external-source', action='store_true',
                       help='Use as external credential provider. Implies -ns option')
    args = parser.parse_args()
    arg_dict = vars(args)

    for arg in ['profile', 'rolearn']:
        if not validate_input(arg, arg_dict[arg]):
            raise ValueError(f'Invalid input for {arg}')

    main(arg_dict)
