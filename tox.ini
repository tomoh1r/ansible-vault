[tox]
envlist = py27, py27-ansible2
setupdir = .

[testenv]
basepython = python2.7

[testenv:py27]
commands = python2.7 setup.py test

[testenv:py27-ansible2]
commands =
    pip install -U git+https://github.com/ansible/ansible.git@stable-2.0#egg=ansible
    python2.7 setup.py test
