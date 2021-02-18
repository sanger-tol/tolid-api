# coding: utf-8

from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.1.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Tree of Life public name API",
    author_email="kh14@sanger.ac.uk",
    url="",
    keywords=["Swagger", "Tree of Life public name API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    API for ToL Public name registry
    """
)
