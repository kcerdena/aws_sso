from aws_sso import __main__ as main


def test_rolearn_missing_is_ok():
    assert main.validate_input('rolearn', None)


def test_rolearn_format_is_ok():
    assert main.validate_input('rolearn', 'arn:aws:iam::123456789012:role/S3Access')


def test_profile_is_ok():
    assert main.validate_input('profile', '123456789012_Test-Profile.Name')
