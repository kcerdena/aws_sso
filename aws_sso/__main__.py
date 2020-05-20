import argparse
import re
import sys
from . import credentials
from . import helper


def main(args):
    if args['discover_roles']:
        credentials.store_awsconfig_external_provider_profiles(args['profile'])
        config_file_path = helper.get_env_var('AWS_CONFIG_FILE', None)
        print(f'Updated named profiles with external credential provider in: {config_file_path}')
        sys.exit()

    cred = credentials.get_role_session_credentials(
        args['profile'], args['rolearn']
    )

    if args['external_source'] and args['rolearn']:
        credentials.print_credentials(cred)
        sys.exit()

    if args['env_vars']:
        credentials.print_export_strings(cred)
        sys.exit()

    credentials.store_default_role_session_credentials(cred)

    credentials_file_path = helper.get_env_var('AWS_SHARED_CREDENTIALS_FILE', None)
    account_id = helper.parse_role_arn(cred['role_arn'])['account_id']
    role_name = helper.parse_role_arn(cred['role_arn'])['role_name']
    expiration = helper.int_to_datetime(cred['expiration']).isoformat()
    x_minutes = helper.minutes_from_now(expiration)
    print(f'Temporary credentials added to {credentials_file_path}')
    print(f'Account: {account_id}')
    print(f'Role:    {role_name}')
    print(f'Expires: {expiration} ({x_minutes}m)')


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
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-env', '--env_vars', action='store_true',
                       help='Environment variable export strings to stdout')
    group.add_argument('-ext', '--external-source', action='store_true',
                       help='Use as external credential provider, Requires --rolearn')
    group.add_argument('-d', '--discover-roles', action='store_true',
                       help='Discover SSO roles and create external credential provider profiles in AWS_CONFIG_FILE')
    args = parser.parse_args()
    arg_dict = vars(args)

    for arg in ['profile', 'rolearn']:
        if not validate_input(arg, arg_dict[arg]):
            raise ValueError(f'Invalid input for {arg}')

    main(arg_dict)
