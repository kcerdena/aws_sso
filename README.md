# aws-sso-credential-provider

Retrieves temporary credentials for programmatic access using AWS SSO roles.

[![build](https://img.shields.io/github/workflow/status/kcerdena/aws_sso/build?style=plastic)](https://github.com/kcerdena/aws_sso/actions?query=workflow%3Abuild) [![Codecov](https://img.shields.io/codecov/c/github/kcerdena/aws_sso?style=plastic&token=91b2881bcee24aeda75bf2f9ad4b0f59)](https://codecov.io/gh/kcerdena/aws_sso) [![PyPI](https://img.shields.io/pypi/v/aws-sso-credential-provider?style=plastic)](https://pypi.org/project/aws-sso-credential-provider/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aws-sso-credential-provider?style=plastic)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=alert_status)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso) [![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=security_rating)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=kcerdena_aws_sso&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=kcerdena_aws_sso)


## Overview
So, you've decided to use [AWS Single Sign-On](https://aws.amazon.com/single-sign-on/) to manage user authentication for multiple AWS accounts. Great idea! Now you can centrally manage user access permissions using the directory of your choosing. As a systems administrator, you're using [AWS CLI version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) with [named profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) to interact with your accounts. Now your custom automation programs fail and are unable to locate credentials!

Named profiles configured for SSO are [only usable by AWS CLIv2](https://docs.aws.amazon.com/credref/latest/refdocs/setting-global-sso_start_url.html). That means your automation using boto3 or other AWS SDK clients fail authentication when referencing these profiles.

This python module solves that problem by retrieving [AWS STS temporary security credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html) for your chosen AWS SSO Role.

## Installation
Requires installation of [AWS CLI version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) for SSO login support.

Requires configuration of (1) [named profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) per SSO directory credential. This profile can be configured with any account and role your SSO credentials provide access to. However, it is recommended you use the lowest permissioned role available. Example aws config file (~/.aws/config) profile:
```text
[profile SSO_PROFILE]
sso_start_url = https://my-sso-portal.awsapps.com/start
sso_role_name = SSOReadOnlyRole
sso_region = us-east-1
sso_account_id = 123456789012
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [aws-sso-credential-provider](https://pypi.org/project/aws-sso-credential-provider/).
```bash
pip install aws-sso-credential-provider
```

## Detail
This python module uses the cached AWS SSO access token to retrieve STS short-term credentials for a specified role.
If the SSO access token is expired, the python module shells out to execute `aws sso login --profile SSO_PROFILE` and renews the token.

## Usage
```bash
# usage: python3 -m aws_sso [-h] -p PROFILE [-r ROLEARN] [-env | -ext | -d]

# optional arguments:
#   -h, --help            show this help message and exit
#   -p PROFILE, --profile PROFILE
#                         Named profile for AWS SSO login
#   -r ROLEARN, --rolearn ROLEARN
#                         RoleArn for session credentials
#   -env, --env_vars      Environment variable export strings to stdout
#   -ext, --external-source
#                         Use as external credential provider, Requires --rolearn
#   -d, --discover-roles  Discover SSO roles and create external credential provider profiles in AWS_CONFIG_FILE
```

### I want to use my AWS SDK programs with named profiles.
Use this python module as an [external credential provider](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html). It will supply your programs with temporary credentials for the SSO role.

The easiest way to configure this is to run the module in discovery mode.
```bash
python3 -m aws_sso -p SSO_PROFILE -d
```
Discovery mode will lookup all accounts and roles available to you using the SSO profile credentials you provided. It then creates or updates a named profile for each RoleARN found. 

If you don't want to use discovery mode, you can edit your AWS config file (~/.aws/config) and add a named profile for each role that you want temporary credentials.
```text
[profile ACCOUNTNUM-ROLENAME]
credential_process = python3 -m aws_sso -p SSO_PROFILE -r ROLEARN -ext
```

To test the named profiles, make a get-caller-identity call for each profile name and observe the Arn change in response.
```bash
aws sts get-caller-identity --profile ACCOUNTNUM-ROLENAME
```

### I don't want to use named profiles.
If you don't want to use named profiles, you can load temporary security credentials into either the default credentials profile, or environment variables.

### I want to interactively choose a role and load temporary security credentials into my default credentials profile.
Overwrites the default profile values in your AWS credentials file (~/.aws/credentials) for these three keys: aws_access_key_id, aws_secret_access_key, and aws_session_token.
```bash
python3 -m aws_sso -p SSO_PROFILE
```
Bypass the account and role chooser by specifying a ROLEARN.
```bash
python3 -m aws_sso -p SSO_PROFILE -r ROLEARN
```
Example AWS credentials file:
```text
[default]
aws_access_key_id = ASIAXXXXXXXXXXXXXXXX
aws_secret_access_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
aws_session_token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### I want to load temporary security credentials into my environment variables.
Environment variables are not available outside the current shell. 
```bash
eval "$(python3 -m aws_sso -p SSO_PROFILE -r ROLEARN -env)"
```
Exports these environment variables:
```bash
export AWS_ACCESS_KEY_ID='ASIAXXXXXXXXXXXXXXXX'
export AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
export AWS_SESSION_TOKEN='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)