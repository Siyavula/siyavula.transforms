from setuptools import setup, find_packages
import os

version = '0.0.0'

requires = [
    'setuptools',
    'lxml',
]

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'docs', 'HISTORY.txt')).read()

setup(name='siyavula.transforms',
      version=version,
      description="A set of transforms for the Siyavula content pipelines.",
      long_description=README + "\n\n" + CHANGES,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Carl Scheffler',
      author_email='carl@siyavula.com',
      url='https://github.com/Siyavula/siyavula.transforms',
      license='Copyright (C) Siyavula Education (Pty) Ltd',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['siyavula'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      test_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
