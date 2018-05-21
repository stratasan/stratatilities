#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'boto3',
    'requests',
    'hvac==0.6.0',
    # TODO: put package requirements here
]

dependency_links=[
    "git+ssh://git@github.com/stratasan/hvac.git@0.6.0#egg=hvac-0.6.0"
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'mock',
]

setup(
    name='stratatilities',
    version='0.1.0',
    description="Various utilities for use across Stratasan services",
    long_description=readme + '\n\n' + history,
    author="Stratasan",
    author_email='dev@stratasan.com',
    url='https://github.com/stratasan/stratatilities',
    packages=find_packages(include=['stratatilities']),
    entry_points={
        'console_scripts': [
            'stratatilities=stratatilities.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    dependency_links=dependency_links,
    license="MIT license",
    zip_safe=False,
    keywords='stratatilities',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
