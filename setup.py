import os

from setuptools import setup, find_packages


def _read(fname):
    here = os.path.dirname(os.path.abspath(__file__))
    return open(os.path.join(here, fname)).read()


setup(
    name='ansible-vault',
    version='1.1.2',
    author='Tomohiro NAKAMURA',
    author_email='quickness.net@gmail.com',
    url='https://github.com/tomoh1r/ansible-vault',
    description='R/W an ansible-vault yaml file',
    long_description=_read('README.rst'),
    packages=find_packages(),
    install_requires=['ansible'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    license='GPLv3',
    extras_require={
        'test': ['pytest'],
        'release': ['twine'],
    }
)
