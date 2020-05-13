import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws_sso-kcerdena",
    version="0.0.1",
    author="Kacey Cerdena",
    author_email="kacey.cerdena@outlook.com",
    description="Session credential provider for AWS SSO roles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kcerdena/aws_sso",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
    ],
    python_requires='>=3.7',
)