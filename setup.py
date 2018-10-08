from __future__ import print_function
from os.path import expanduser,isdir, isfile
from setuptools import setup


#import h5py
#import numpy as np
import glob

setup(name='HiFiPy',
	version='0.1',
	description='Python software for analysis of HiFi simulations.',
	url='https://github.com/HiFiPy/HiFiPy',
	author='Nicholas A. Murphy',
	author_email='namurphy@cfa.harvard.edu',
	license='BSD-3-clause',
	packages=['hifipy','hifipy.io'],
	install_requires=['numpy','h5py'],
	include_package_data=True
	)