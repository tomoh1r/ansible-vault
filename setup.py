import sys
import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


def _read(fname):
    here = os.path.dirname(os.path.abspath(__file__))
    return open(os.path.join(here, fname)).read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
        if len(sys.argv) == 2:
            self.pytest_args = ['ansible_vault']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        sys.exit(pytest.main(self.pytest_args))


setup(
    name='ansible-vault',
    version='1.0.5',
    author='Tomohiro NAKAMURA',
    author_email='quickness.net@gmail.com',
    url='https://github.com/tomoh1r/ansible-vault',
    description='R/W an ansible-vault yaml file',
    long_description=_read('README.rst'),
    packages=find_packages(),
    install_requires=['ansible'],
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    license='GPLv3',
    extras_require = {
        'test': ['pytest', 'testfixtures'],
    }
)
