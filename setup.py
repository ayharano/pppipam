"""PPPIPAM's setup script."""

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pppipam',  # Required
    version='0.1.0',  # Required
    description="Poor person's Python IP Address Manager",  # Required
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional
    url='https://github.com/ayharano/pppipam',  # Optional
    author='Alexandre Harano',  # Optional
    author_email='alexandre@harano.net.br',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
    ],
    keywords='ip address management ipv4 ipv6 network system administration',  # Optional
    packages=find_packages(exclude=['tests']),  # Required
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/ayharano/pppipam/issues',
        'Source': 'https://github.com/ayharano/pppipam',
    },
    python_requires='>=3.7, <4',  # Optional
)
