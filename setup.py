from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.4'
DESCRIPTION = 'Air Traffic Control Simulator'
LONG_DESCRIPTION = 'A package that allows to use ATC simulator'

# Setting up
setup(
    name="ATC Simulator",
    version=VERSION,
    author="Rahul Kantwa",
    author_email="<ce18b024@iittp.ac.in>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['beautifultable', 'pymongo'],
    keywords=['ATC'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)