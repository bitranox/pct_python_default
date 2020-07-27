Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

please check `SemVer <https://semver.org/>`_ for more information on versioning

tasks:
    - github integration
    - travis cleanup
    - build against active github branch, not master
    - multiple bdists to pypi
    - arm64
    - build test project

0.1.2a
------
2020-07-23 : development
    - add STDOUT, STDERR to cli output on flag --traceback
    - main file, error message "this is a library only..." to sys.stderr
    - put example to include description from code, with nice format for pycharm help
    - make cli_exit_tools an external pypi module

0.1.1
-----
2020-07-17 : feature release
    - improve message per imported secret for travis
    - bump code coverage
    - added PizzaCutter.date
    - added version hint on top and internal hyperlink for changelog

0.1.0
----------
2020-07-16 : initial public release
