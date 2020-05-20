import configparser
from aws_sso import credentials
from botocore.exceptions import ParamValidationError


def test_should_retrieve_creds_without_access_token(mocker):
    mocker.patch.object(credentials, 'file_handler')
    mocker.patch.object(credentials, 'sso_util')
    credentials.file_handler.get_sso_access_token.side_effect = [
        'BADTOKEN', 'GOODTOKEN']
    credentials.sso_util.get_account_list.side_effect = mock_test_access_token_response
    credentials.sso_util.get_role_credentials.side_effect = mock_get_role_credentials_response
    role_arn = get_readonly_role_arn()

    cred = credentials.get_role_session_credentials('sso-profile', role_arn)

    assert cred == get_cred()
    assert credentials.file_handler.get_sso_access_token.call_count == 2
    assert credentials.sso_util.get_account_list.call_count == 2
    credentials.sso_util.get_account_list.assert_called_with('GOODTOKEN')
    assert credentials.sso_util.exec_login.call_count == 1
    credentials.sso_util.exec_login.assert_called_with('sso-profile')
    assert credentials.sso_util.get_account_id.call_count == 0
    assert credentials.sso_util.get_role_name.call_count == 0
    assert credentials.sso_util.get_role_arn.call_count == 0
    assert credentials.sso_util.get_role_credentials.call_count == 1
    credentials.sso_util.get_role_credentials.assert_called_with(
        'GOODTOKEN', role_arn)


def test_should_retrieve_creds_without_role_arn(mocker):
    mocker.patch.object(credentials, 'file_handler')
    mocker.patch.object(credentials, 'sso_util')
    credentials.file_handler.get_sso_access_token.side_effect = [
        'BADTOKEN', 'GOODTOKEN']
    credentials.sso_util.get_account_list.side_effect = mock_test_access_token_response
    credentials.sso_util.get_account_id.side_effect = mock_get_account_id
    credentials.sso_util.get_role_name.side_effect = mock_get_role_name
    credentials.sso_util.get_role_credentials.side_effect = mock_get_role_credentials_response
    role_arn = get_readonly_role_arn()

    cred = credentials.get_role_session_credentials('sso-profile')

    assert cred == get_cred()
    assert credentials.file_handler.get_sso_access_token.call_count == 2
    assert credentials.sso_util.get_account_list.call_count == 2
    credentials.sso_util.get_account_list.assert_called_with('GOODTOKEN')
    assert credentials.sso_util.exec_login.call_count == 1
    credentials.sso_util.exec_login.assert_called_with('sso-profile')
    assert credentials.sso_util.get_account_id.call_count == 1
    credentials.sso_util.get_account_id.assert_called_with('GOODTOKEN')
    assert credentials.sso_util.get_role_name.call_count == 1
    credentials.sso_util.get_role_name.assert_called_with(
        'GOODTOKEN', '111111111111')
    assert credentials.sso_util.get_role_credentials.call_count == 1
    credentials.sso_util.get_role_credentials.assert_called_with(
        'GOODTOKEN', role_arn)


def test_should_store_session_creds_to_new_credentials_file(mocker):
    cred = get_cred()
    new_cred_config = configparser.ConfigParser(default_section='default')
    mocker.patch.object(credentials, 'file_handler')
    credentials.file_handler.get_credentials_config.return_value = new_cred_config

    credentials.store_default_role_session_credentials(cred)

    expected_cred_config = get_cred_config()
    assert credentials.file_handler.get_credentials_config.call_count == 1
    credentials.file_handler.write_credentials_config.assert_called_with(
        expected_cred_config)
    assert credentials.file_handler.write_credentials_config.call_count == 1


def test_should_store_session_creds_to_existing_credentials_file(mocker):
    cred = get_cred()
    existing_cred_config = configparser.ConfigParser(default_section='default')
    existing_cred_config['default']['aws_access_key_id'] = 'EXPIREDACCESSKEY'
    existing_cred_config['default']['aws_secret_access_key'] = 'EXPIREDSECRETACCESSKEY'
    existing_cred_config['default']['aws_session_token'] = 'EXPIREDSESSIONTOKEN'
    mocker.patch.object(credentials, 'file_handler')
    credentials.file_handler.get_credentials_config.return_value = existing_cred_config

    credentials.store_default_role_session_credentials(cred)

    expected_cred_config = get_cred_config()
    assert credentials.file_handler.get_credentials_config.call_count == 1
    credentials.file_handler.write_credentials_config.assert_called_with(
        expected_cred_config)
    assert credentials.file_handler.write_credentials_config.call_count == 1


def test_should_print_environment_vars_to_stdout(capsys):
    cred = get_cred()
    credentials.print_export_strings(cred)
    captured = capsys.readouterr()
    assert captured.out == "export AWS_ACCESS_KEY_ID='ASIAXXXXXXXXXXXXXXXX'\n" \
        "export AWS_SECRET_ACCESS_KEY='SAK_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'\n" \
        "export AWS_SESSION_TOKEN='SessionToken_/ZwhaXZU0E2JRVqcg9ESMr6XNg='\n"


def test_should_print_external_credential_process_to_stdout(capsys):
    cred = get_cred()
    credentials.print_credentials(cred)
    captured = capsys.readouterr()
    assert captured.out == '{"Version":1,"AccessKeyId":"ASIAXXXXXXXXXXXXXXXX",' \
        '"SecretAccessKey":"SAK_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",' \
        '"SessionToken":"SessionToken_/ZwhaXZU0E2JRVqcg9ESMr6XNg=",' \
        '"Expiration":"2020-05-12T04:44:21+00:00"}\n'


def test_should_store_external_credential_provider_profiles(mocker):
    mocker.patch.object(credentials, 'file_handler')
    mocker.patch.object(credentials, 'sso_util')
    credentials.file_handler.get_sso_access_token.side_effect = ['GOODTOKEN']
    credentials.sso_util.get_account_list.side_effect = mock_test_access_token_response
    credentials.sso_util.get_rolearn_list.return_value = get_rolearn_list_test_data()
    credentials.file_handler.get_awsconfig_config.return_value = get_config()

    credentials.store_awsconfig_external_provider_profiles('sso-profile')

    credentials.file_handler.write_awsconfig_config.assert_called_with(
        get_expected_awsconfig())


def get_expected_awsconfig():
    config = get_config()
    config.add_section('111111111111_ReadOnly')
    config['111111111111_ReadOnly']['credential_process'] = \
        'python3 -m aws_sso -p sso-profile -r arn:aws:iam::111111111111:role/ReadOnly -ext'
    config.add_section('111111111111_Admin')
    config['111111111111_Admin']['credential_process'] = \
        'python3 -m aws_sso -p sso-profile -r arn:aws:iam::111111111111:role/Admin -ext'
    config.add_section('222222222222_ReadOnly')
    config['222222222222_ReadOnly']['credential_process'] = \
        'python3 -m aws_sso -p sso-profile -r arn:aws:iam::222222222222:role/ReadOnly -ext'
    config.add_section('222222222222_Admin')
    config['222222222222_Admin']['credential_process'] = \
        'python3 -m aws_sso -p sso-profile -r arn:aws:iam::222222222222:role/Admin -ext'
    return config


def get_rolearn_list_test_data():
    return ['arn:aws:iam::111111111111:role/ReadOnly',
            'arn:aws:iam::111111111111:role/Admin',
            'arn:aws:iam::222222222222:role/ReadOnly',
            'arn:aws:iam::222222222222:role/Admin'
            ]


def get_readonly_role_arn():
    return 'arn:aws:iam::111111111111:role/ReadOnly'


def get_cred():
    cred = {}
    cred['accessKeyId'] = 'ASIAXXXXXXXXXXXXXXXX'
    cred['secretAccessKey'] = 'SAK_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    cred['sessionToken'] = 'SessionToken_/ZwhaXZU0E2JRVqcg9ESMr6XNg='
    cred['expiration'] = 1589258661000
    cred['role_arn'] = get_readonly_role_arn()
    return cred


def get_config():
    return configparser.ConfigParser(default_section='default')


def get_cred_config():
    config = get_config()
    config['default']['aws_access_key_id'] = 'ASIAXXXXXXXXXXXXXXXX'
    config['default']['aws_secret_access_key'] = 'SAK_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    config['default']['aws_session_token'] = 'SessionToken_/ZwhaXZU0E2JRVqcg9ESMr6XNg='
    return config


def mock_test_access_token_response(access_token):
    if access_token == 'BADTOKEN':
        raise ParamValidationError(report='')


def mock_get_role_credentials_response(access_token, role_arn):
    if access_token == 'GOODTOKEN' and role_arn == get_readonly_role_arn():
        return get_cred()
    else:
        return None


def mock_get_account_id(access_token):
    if access_token == 'GOODTOKEN':
        return '111111111111'
    else:
        return None


def mock_get_role_name(access_token, account_id):
    if access_token == 'GOODTOKEN' and account_id == '111111111111':
        return 'ReadOnly'
    else:
        return None


def mock_get_role_arn(account_id, role_name):
    if account_id == '111111111111' and role_name == 'ReadOnly':
        return 'arn:aws:iam::111111111111:role/ReadOnly'
    else:
        return None
