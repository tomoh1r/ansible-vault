from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="ansible-vault",
    version="3.1.0",
    author="Tomohiro NAKAMURA",
    author_email="quickness.net@gmail.com",
    url="https://github.com/tomoh1r/ansible-vault",
    description="R/W an ansible-vault yaml file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["setuptools", "ansible"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    license="GPLv3",
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "coveralls",
            "flake8",
            "black",
            "isort[pyproject]",
            "pylint",
        ],
        "release": ["build", "twine"],
    },
)
