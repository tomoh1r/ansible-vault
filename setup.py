import os
from setuptools import setup


def _read(fname):
    here = os.path.dirname(os.path.abspath(__file__))
    return open(os.path.join(here, fname)).read()


setup(
    name='ansible-vault',
    version='1.0.0',
    author='Tomohiro NAKAMURA',
    author_email='quickness.net@gmail.com',
    description='R/W an ansible-vault yaml file',
    long_description=_read('README.rst'),
    package=['ansible_vault'],
    install_requires=['ansible'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    license='GPLv3',
)
