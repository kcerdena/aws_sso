# aws-sso-credential-provider

Retrieves temporary credentials for programmatic access using AWS SSO roles.

[![build](https://img.shields.io/github/workflow/status/kcerdena/aws_sso/build?style=plastic)](https://github.com/kcerdena/aws_sso/actions?query=workflow%3Abuild) [![Codecov](https://img.shields.io/codecov/c/github/kcerdena/aws_sso?style=plastic&token=91b2881bcee24aeda75bf2f9ad4b0f59)](https://codecov.io/gh/kcerdena/aws_sso) [![PyPI](https://img.shields.io/pypi/v/aws-sso-credential-provider?style=plastic)](https://pypi.org/project/aws-sso-credential-provider/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aws-sso-credential-provider?style=plastic)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=alert_status)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=security_rating)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso)


## Overview
So, you've decided to use [AWS Single Sign-On](https://aws.amazon.com/single-sign-on/) to manage user authentication for multiple AWS accounts. Great idea! Now you can centrally manage user access permissions using the directory of your choosing. As a systems administrator, you're using [AWS CLI version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) with [named profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) to interact with your accounts. Now your custom automation programs fail and are unable to locate credentials!

Named profiles configured for SSO are [only usable by AWS CLIv2](https://docs.aws.amazon.com/credref/latest/refdocs/setting-global-sso_start_url.html). That means your automation using boto3 or other AWS SDK clients fail authentication when referencing these profiles.

This python module solves that problem by retrieving [AWS STS temporary security credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) for your chosen AWS SSO Role.

## Installation
-Requires installation of [AWS CLI version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) for SSO login support.

-Requires configuration of (1) [named profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) per SSO directory credential. This profile can be configured with any account and role your SSO credentials provide access to. However, it is recommended you use the lowest permissioned role available. Example aws config file (~/.aws/config) profile:
```text
[profile SSO_PROFILE]
sso_start_url = https://my-sso-portal.awsapps.com/start
sso_role_name = SSOReadOnlyRole
sso_region = us-east-1
sso_account_id = 123456789012
```
-Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [aws-sso-credential-provider](https://pypi.org/project/aws-sso-credential-provider/).
```bash
pip install aws-sso-credential-provider
```

## Detail
This python module uses the cached AWS SSO access token to retrieve STS short-term credentials for a specified role.
If the SSO access token is expired, the python module shells out to execute `aws sso login --profile SSO_PROFILE` and renews the token.

## Usage
```bash
# usage: python3 -m aws_sso [-h] -p PROFILE [-r ROLEARN] [-ns] [-env | -ext]

# optional arguments:
#   -h, --help            show this help message and exit
#   -p PROFILE, --profile PROFILE
#                         Named profile for AWS SSO login
#   -r ROLEARN, --rolearn ROLEARN
#                         RoleArn for session credentials
#   -ns, --no-store-creds
#                         Disable output of session credential to AWS_SHARED_CREDENTIALS_FILE
#   -env, --env_vars      Output session credential environment variable export strings
#   -ext, --external-source
#                         Use as external credential provider. Implies -ns option
```

### I want to configure a named profile that works with my programs.
Edit your AWS config file (~/.aws/config) and add a named profile for the role you want to assume.
Configures this program as an [external credential provider](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html). Returns temporary security credentials for the specified RoleARN when the profile is referenced.
```text
[profile ACCOUNTNUM_ROLENAME]
credential_process = python3 -m aws_sso -p SSO_PROFILE -r ROLEARN -ext
```

### I want to interactively choose a role to load into my default credentials profile.
Overwrites the default profile in your AWS credentials file (~/.aws/credentials).
```bash
python3 -m aws_sso -p SSO_PROFILE
```
Example:
```text
[default]
aws_access_key_id = ASIAXXXXXXXXXXXXXXXX
aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
aws_session_token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### I want to load temporary security credentials into my environment variables without modifying the credentials file.
Environment variables are not available outside the current shell. 
```bash
eval "$(python3 -m aws_sso -p SSO_PROFILE -r ROLEARN -env -ns)"
```
Exports these environment variables:
- *AWS_ACCESS_KEY_ID*
- *AWS_SECRET_ACCESS_KEY*
- *AWS_SESSION_TOKEN*

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)