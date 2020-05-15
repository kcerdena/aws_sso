# aws-sso-credential-provider

Retrieves temporary credentials for programmatic access using AWS SSO roles.

[![build](https://img.shields.io/github/workflow/status/kcerdena/aws_sso/build?style=plastic)](https://github.com/kcerdena/aws_sso/actions?query=workflow%3Abuild)
[![Codecov](https://img.shields.io/codecov/c/github/kcerdena/aws_sso?style=plastic&token=91b2881bcee24aeda75bf2f9ad4b0f59)](https://codecov.io/gh/kcerdena/aws_sso)
[![PyPI](https://img.shields.io/pypi/v/aws-sso-credential-provider?style=plastic)](https://pypi.org/project/aws-sso-credential-provider/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aws-sso-credential-provider?style=plastic)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=alert_status)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=security_rating)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso)


## Installation

Requires installation of [AWS CLI version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) for SSO support.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install aws-sso-credential-provider.

```bash
pip install aws-sso-credential-provider
```

## Usage
```bash
usage: python -m aws_sso [-h] -p PROFILE [-r ROLEARN] [-ns] [-env | -ext]

optional arguments:
  -h, --help            show this help message and exit
  -p PROFILE, --profile PROFILE
                        Named profile for AWS SSO login
  -r ROLEARN, --rolearn ROLEARN
                        RoleArn for session credentials
  -ns, --no-store-creds
                        Disable output of session credential to AWS_SHARED_CREDENTIALS_FILE
  -env, --env_vars      Output session credential environment variable export strings
  -ext, --external-source
                        Use as external credential provider. Implies -ns option

```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)