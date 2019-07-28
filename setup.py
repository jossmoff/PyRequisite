#!/usr/local/bin python3
from setuptools import setup, find_packages
from PyRequisite import __version__ as version
setup(name='PyRequisite',
      python_requires='>=3.6',
      version=version,
      description='Find library prerequisites for Python projects.',
      url='https://github.com/JossMoff/PyRequisite',
      author='Joss Moffatt',
      author_email='joss.moffatt@student.manchester.ac.uk',
      license='MIT',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'PyRequisite = PyRequisite.__main__:main']},
      zip_safe=False)
