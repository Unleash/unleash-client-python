"""Setup file for UnleashClient"""
from setuptools import setup, find_packages


def readme():
    """Include README.rst content in PyPi build information"""
    with open('README.md') as file:
        return file.read()

setup(
    name='UnleashClient',
    version='2.0.0',
    author='Ivan Lee',
    author_email='ivanklee86@gmail.com',
    description='Python client for the Unleash feature toggle system!',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/Unleash/unleash-client-python',
    packages=find_packages(),
    install_requires=["requests==2.20.0",
                      "fcache==0.4.7",
                      "mmh3==2.5.1",
                      "apscheduler==3.5.3"],
    tests_require=['pytest', "mimesis", "responses"],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ]
)

