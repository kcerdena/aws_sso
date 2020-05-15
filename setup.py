import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-sso-credential-provider",
    version="0.0.5",
    author="Kacey Cerdena",
    author_email="6180729+kcerdena@users.noreply.github.com",
    description="Session credential provider for AWS SSO roles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kcerdena/aws_sso",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Topic :: System :: Systems Administration"
    ],
    install_requires=[
        'python-dateutil>=2.8',
        'boto3>=1.13'
    ],
    python_requires='>=3.6',
)
