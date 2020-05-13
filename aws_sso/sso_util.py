import subprocess
import boto3
from . import helper

client = boto3.client('sso')


def exec_login(sso_profile):
    return subprocess.run([f'aws sso login --profile {sso_profile}'],
                          shell=True, check=True, capture_output=True)


def get_account_list(access_token):
    response = client.list_accounts(accessToken=access_token)
    return response['accountList']


def get_account_id(access_token):
    account_list = get_account_list(access_token)
    if len(account_list) == 0:
        raise IndexError('No accounts found')
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
        raise IndexError('No roles found')
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
        role_arn = helper.get_role_arn(account_id, role_name)
        print(f"[{x}] {role_name} {role_arn}")
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
    account_id = helper.parse_role_arn(role_arn)['account_id']
    role_name = helper.parse_role_arn(role_arn)['role_name']
    response = client.get_role_credentials(
        accessToken=access_token,
        accountId=account_id,
        roleName=role_name
    )
    response['roleCredentials']['role_arn'] = role_arn
    return response['roleCredentials']
