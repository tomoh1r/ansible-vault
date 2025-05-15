from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="ansible-vault",
    version="4.0.1",
    author="Tomohiro NAKAMURA",
    author_email="quickness.net@gmail.com",
    url="https://github.com/tomoh1r/ansible-vault",
    description="R/W an ansible-vault yaml file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["ansible-core>=2.16", "PyYAML>=5.1"],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Development Status :: 5 - Production/Stable",
    ],
    license="GPL-3.0-or-later",
    extras_require={
        "dev": [
            "setuptools",
            "pytest",
            "pytest-cov",
            "coveralls",
            "flake8",
            "black",
            "isort",
            "pylint",
            "pylint-pytest",
        ],
        "release": ["build", "twine"],
    },
)
