#!/usr/bin/env python
import os
import sys
import io

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# from pip.req import parse_requirements
# from pip.download import PipSession

# Make sure we're actually in the directory containing setup.py.
root_dir = os.path.dirname(__file__)

if root_dir != "":
    os.chdir(root_dir)

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        # pylint: disable=attribute-defined-outside-init
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        #pylint: disable=assignment-from-no-return
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

# install_requires = [str(ir.req) for ir in parse_requirements('requirements.txt', session=PipSession())]

with open('requirements.txt', 'r') as f:
    install_requires = [x.strip() for x in f.readlines()]

setup(name='jcloud',
      version='0.0.1',
      description='Jinja2 Cloud Formation',
      long_description=read('README.md'),
      author='Daniel Lau',
      author_email='jetzdax@dclau.com',
      url='https://github.com/jetzdax/jcloud',
      packages=find_packages(),
      include_package_data=True,
      install_requires=install_requires,
      entry_points={
          'console_scripts': [
              'jcloud = jcloud.cmdline:main'
          ]
      },
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: Other/Proprietary License",
          "Natural Language :: English",
          "Operating System :: Unix",
          "Programming Language :: Python",
          "Topic :: Software Development",
      ],
      tests_require=['tox'],
      cmdclass={'test': Tox})
