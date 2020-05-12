import sys
import argparse
from . import credentials


def main(args):
    cred = credentials.get_role_session_credentials(
        args['profile'], args['rolearn']
    )
    if args['no_store_creds']:
        pass
    else:
        credentials.store_default_role_session_credentials(cred)
    if args['env_vars']:
        credentials.print_export_strings(cred)
    if args['external_source']:
        credentials.print_credentials(cred)


if __name__ == '__main__':
    description = ''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', '--profile', required=True,
                        help='Named profile for AWS SSO login')
    parser.add_argument('-r', '--rolearn',
                        help='RoleArn for session credentials')
    parser.add_argument('-ns', '--no-store-creds', action='store_true',
                        help='Disable output of session credential to ~/.aws/credentials')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-env', '--env_vars', action='store_true',
                       help='Output session credential environment variable export strings')
    group.add_argument('-ext', '--external-source', action='store_true',
                       help='Use as external credential provider')
    args = parser.parse_args()
    main(vars(args))
