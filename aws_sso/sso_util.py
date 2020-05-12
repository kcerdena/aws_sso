import subprocess
import boto3

client = boto3.client('sso')


def exec_login(profile):
    return subprocess.run([f'aws sso login --profile {profile}'], shell=True, check=True, capture_output=True)


def test_access_token(access_token):
    client.list_accounts(accessToken=access_token)


def get_account_id(access_token):
    response = client.list_accounts(
        accessToken=access_token
    )
    account_list = response['accountList']
    if len(account_list) == 0:
        raise Exception('No accounts found')
    elif len(account_list) == 1:
        account = account_list[0]
    else:
        account = __select_account(account_list)
    return account['accountId']


def __select_account(account_list):
    x = 0
    print('Select an account:')
    for account in account_list:
        x += 1
        print(f"[{x}] {account['accountName']} {account['accountId']}")
    index = __select_entry(x) - 1
    return account_list[index]


def get_role_name(access_token, account_id):
    response = client.list_account_roles(
        accessToken=access_token,
        accountId=account_id
    )
    role_list = response['roleList']
    if len(role_list) == 0:
        raise Exception('No roles found')
    elif len(role_list) == 1:
        role = role_list[0]
    else:
        role = __select_role(account_id, role_list)
    return role['roleName']


def __select_role(account_id, role_list):
    x = 0
    print('Select a role:')
    for role in role_list:
        x += 1
        role_name = role['roleName']
        print(f"[{x}] {role_name} {get_role_arn(account_id, role_name)}")
    index = __select_entry(x) - 1
    return role_list[index]


def __select_entry(max_value):
    while True:
        try:
            selection = int(input(f'Enter [1-{max_value}]:'))
            if selection < 1 or selection > max_value:
                raise ValueError
        except ValueError:
            print('Unrecognized value')
            continue
        else:
            break
    return selection


def get_role_credentials(access_token, role_arn):
    account_role = parse_role_arn(role_arn)
    response = client.get_role_credentials(
        accessToken=access_token,
        accountId=account_role['account_id'],
        roleName=account_role['role_name']
    )
    response['roleCredentials']['role_arn'] = role_arn
    return response['roleCredentials']


def get_role_arn(account_id, role_name):
    return f'arn:aws:iam::{account_id}:role/{role_name}'


def parse_role_arn(role_arn):
    arn_parts = role_arn.split(':')
    return {
        'account_id': arn_parts[4],
        'role_name': arn_parts[5].lstrip('role/')
    }