from setuptools import setup, find_packages


setup(
    name="platform42",
    version='0.1dev',
    description='Programatic access to the Code42 paltform api',
    long_description=open('README.md').read(),
    author="Andrew Helgeson",
    author_email="andrew.w.helgeson@gmail.com",
    packages=find_packages(exclude="code42/tests"),
    url='http://pypi.python.org/pypi/platform42',
    license='LICENSE.txt',
    install_requires=[
        "requests >= 2.0.0"
        ]
    )
