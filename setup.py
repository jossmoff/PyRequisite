from setuptools import setup
from PyRequisite import __version__ as version
setup(name='PyRequisite',
      version=version,
      description='Find library prerequisites for Python projects.',
      url='https://github.com/JossMoff/PyRequisite',
      author='Joss Moffatt',
      author_email='joss.moffatt@student.manchester.ac.uk',
      license='MIT',
      packages=['PyRequisite'])
