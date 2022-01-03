"""Setup file for UnleashClient"""
from setuptools import setup, find_packages


def readme():
    """Include README.rst content in PyPi build information"""
    with open('README.md') as file:
        return file.read()


setup(
    name='UnleashClient',
    version='5.0.0',
    author='Ivan Lee',
    author_email='ivanklee86@gmail.com',
    description='Python client for the Unleash feature toggle system!',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/Unleash/unleash-client-python',
    packages=find_packages(exclude=["tests*"]),
    package_data={"UnleashClient": ["py.typed"]},
    install_requires=["requests", "fcache", "mmh3", "apscheduler"],
    tests_require=['pytest', "mimesis", "responses", 'pytest-mock'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)
