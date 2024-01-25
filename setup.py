from setuptools import setup, find_packages

setup(
    name='aes_encryption',
    version='0.1.1',
    packages=find_packages(),
    description='A simple AES encryption library',
    author='TIAA - API Security',
    author_email='',
    keywords='encryption aes cryptography',
    install_requires=[
        'cryptography>=3.0'
    ]
)