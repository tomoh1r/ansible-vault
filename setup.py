import os

from setuptools import find_packages, setup


def _read(fname):
    here = os.path.dirname(os.path.abspath(__file__))
    return open(os.path.join(here, fname)).read()


setup(
    name="ansible-vault",
    version="2.1.0",
    author="Tomohiro NAKAMURA",
    author_email="quickness.net@gmail.com",
    url="https://github.com/tomoh1r/ansible-vault",
    description="R/W an ansible-vault yaml file",
    long_description=_read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["setuptools", "ansible"],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    license="GPLv3",
    extras_require={
        "dev": ["pytest"],
        'dev:python_version>="3.6"': ["flake8", "black", "isort[pyproject]"],
        "release": ["twine"],
    },
)
