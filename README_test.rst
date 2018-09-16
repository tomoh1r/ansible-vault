===========
how to test
===========

1. Create virtualenv.

   .. code-block:: console

      $ virtualenv venvtest

2. Update dependencies.

   .. code-block:: console

      $ ./venvtest/bin/python -m pip install -e '.[dev]'

3. Run test.

   .. code-block:: console

      $ ./venvtest/bin/python -m pytest
