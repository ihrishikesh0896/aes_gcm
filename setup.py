from setuptools import setup, find_packages

setup(
    name='aesgcm',
    version='0.1.1',
    packages=find_packages(),
    description='A simple AES encryption library',
    author='Hrishikesh Nate',
    author_email='ihrishikeshnate@gmail.com',
    keywords='encryption aes cryptography',
    install_requires=[
        'cryptography>=3.0'
    ]
)