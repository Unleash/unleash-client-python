"""Setup file for UnleashClient"""
from setuptools import setup, find_packages


def readme():
    """Include README.rst content in PyPi build information"""
    with open('README.md') as file:
        return file.read()


setup(
    name='UnleashClient',
    version='0.0.1',
    description='Python client for the wonderful unleash feature flag framework!',
    long_description=readme(),
    url='https://github.com/ivanklee86/UnleashClient',
    author='Ivan Lee',
    author_email='ivanklee86@gmail.com',
    packages=find_packages(),
    install_requires=["requests"],
    tests_require=['pytest'],
    zip_safe=False,
    include_package_data=True
)
