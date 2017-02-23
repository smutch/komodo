#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=6.0',
    'numpy>=1.11.2',
    'astropy>=1.1.1',
]

setup(
    name='komodo',
    py_modules=['komodo'],
    version='0.1',
    description="Useful cmdline tasks related to the Meraxes semi-analytic model.",
    long_description=readme,
    author="Simon Mutch",
    author_email='smutch.astro@gmail.com',
    url='https://github.com/smutch/komodo',
    entry_points={
        'console_scripts': [
            'komodo=komodo:komodo'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='komodo',
    classifiers=[
        'Development Status :: 3 - Alpha'
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
)
