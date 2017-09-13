---
language: python
sudo: false
cache:
  directories:
    - $HOME/.cache/pip
python:
  - "2.7"
  - "3.3"
  - "3.4"
  - "3.5"
  - "3.6"
install:
  - python -m pip install -U setuptools pip
  - python setup.py setup_test
script:
  - python -m pytest
  - if [ "$TRAVIS_PYTHON_VERSION" == '2.7' ] ; then python -m pip install -U 'ansible<2.0.0' && python -m pytest ; fi

# vim:st=2 sts=2 sw=2:
