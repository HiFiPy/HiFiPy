from setuptools import setup


setup(
	name='HiFiPy',
	version='0.1',
	description='Python software for analysis of HiFi simulations.',
	url='https://github.com/HiFiPy/HiFiPy',
	author='Nicholas A. Murphy and Eric S. Mukherjee',
	author_email='namurphy@cfa.harvard.edu',
	license='BSD-3-clause',
	packages=['hifipy','hifipy.io'],
	install_requires=['numpy', 'scipy', 'h5py'],
	include_package_data=True,
	setup_requires = ["pytest-runner", "h5py", "numpy"],
	tests_require = ["pytest", "h5py", "numpy"],
)