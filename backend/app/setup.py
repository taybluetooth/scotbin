import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Which Bin?",
    version = "0.0.1",
    author = "Callum Taylor",
    author_email = "callumtaylorbusiness@gmail.com",
    description = ("An application which instructs a user on which rubbish bin to put outside."),
    license = "MIT",
    keywords = "Scotland Scottish Bin Rubbish Trash Automation",
    packages=['helpers', 'councils', 'constants'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)