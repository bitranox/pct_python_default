Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes

tasks:
    - multiple bdists to pypi
    - arm64


0.1.0
----------
2020-??-?? : initial public release
    - fix setup.py for deploy on pypi
    - fix travis for pypi deploy testing
    - mypy --no-warn-unused-ignores in travis (this should be tested locally)
    - mypy.ini warn-unused-ignores = False (this should be tested locally)
