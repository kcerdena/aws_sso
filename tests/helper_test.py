from aws_sso import helper


def test_should_return_default_awsconfig(mocker):
    mocker.patch.object(helper, 'environ')
    result = helper.get_env_var('AWS_CONFIG_FILE', None)
    assert result == '~/.aws/config'


def test_should_return_default_credentials(mocker):
    mocker.patch.object(helper, 'environ')
    result = helper.get_env_var('AWS_SHARED_CREDENTIALS_FILE', None)
    assert result == '~/.aws/credentials'


def test_should_return_environment_variable(mocker):
    mocker.patch.dict(helper.environ, {'AWS_SHARED_CREDENTIALS_FILE': '~/alternate/credentials'})
    result = helper.get_env_var('AWS_SHARED_CREDENTIALS_FILE', None)
    assert result == '~/alternate/credentials'


def test_should_return_parameter():
    result = helper.get_env_var('AWS_CONFIG_FILE', '~/alternate/config')
    assert result == '~/alternate/config'
