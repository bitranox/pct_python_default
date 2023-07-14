Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

please check `SemVer <https://semver.org/>`_ for more information on versioning

v1.0.5
---------
2023-07-14:
    - add codeql badge
    - move 3rd_party_stubs outside the src directory
    - add pypy 3.10 tests
    - add python 3.12-dev tests

v1.0.4
---------
2023-07-13:
    - require minimum python 3.8
    - remove python 3.7 tests

v1.0.3
---------
2023-07-13:
    - introduce PEP517 packaging standard
    - introduce pyproject.toml build-system
    - remove mypy.ini
    - remove pytest.ini
    - remove setup.cfg
    - remove setup.py
    - remove .bettercodehub.yml
    - remove .travis.yml
    - update black config
    - clean ./tests/test_cli.py


v1.0.2
---------
2023-01-13:
    - update github actions : checkout@v3 and setup-python@v4
    - remove "better code" badges
    - remove python 3.6 tests
    - add python 3.11 tests
    - update to pypy 3.9 tests

1.0.1b
-------
work in progress
    - add mypy options to install missing types '--install-types'

1.0.0
-------
2021-11-22 : Major Release
    - implement github actions
    - fix "setup.py test"
    - implement check for test environment on __init__

0.1.6
-------
2020-07-30 : release
    - fix pypi deploy

0.1.5
-------
2020-07-30 : release
    - add helper "find_version_number_in_file"

0.1.4
-------
2020-07-29 : release
    - put package name in travis env


0.1.3
-------
2020-07-29 : release
    - delete wrong parameter pytest.ini --doctest-glob
    - add MYPYPATH in travis.yml
    - add 3rd_party_stubs directory

0.1.2
------
2020-07-29 : release
    - add STDOUT, STDERR to cli output on flag --traceback
    - main file, error message "this is a library only..." to sys.stderr
    - put example to include description from code, with nice format for pycharm help
    - make cli_exit_tools an external pypi module
    - new travis matrix, using lib_travis

0.1.1
-----
2020-07-17 : release
    - improve message per imported secret for travis
    - bump code coverage
    - added PizzaCutter.date
    - added version hint on top and internal hyperlink for changelog

0.1.0
----------
2020-07-16 : initial public release
