#!/usr/bin/env python3

from setuptools import setup

setup(name='collector',
      version='0.0.1',
      description='IPFIX Collector for OVS Project',
      author='wdavid12',
      author_email='wdavid12@campus.technion.ac.il',
      url='http://github.com/wdavid12/python-collector',
      packages=['collector'],
      install_requires=['ipfix'],
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: "
                   "GNU Lesser General Public License v3 or later (LGPLv3+)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3.3",
                   "Topic :: System :: Networking"],
      )

