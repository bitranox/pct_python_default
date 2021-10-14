# STDLIB
import os
import pathlib
import sys

name = '{{PizzaCutter.name}}'
title = '{{PizzaCutter.title}}'
version = '{{PizzaCutter.version}}'
url = '{{PizzaCutter.url}}'
author = '{{PizzaCutter.author}}'
author_email = '{{PizzaCutter.author_email}}'
shell_command = '{{PizzaCutter.shell_command}}'


def print_info() -> None:
    print("""\

Info for {{PizzaCutter.project_name}}:

    {{PizzaCutter.title}}

    Version : {{PizzaCutter.version}}
    Url     : {{PizzaCutter.url}}
    Author  : {{PizzaCutter.author}}
    Email   : {{PizzaCutter.author_email}}""")


def is_doctest_running() -> bool:
    """
    >>> if not is_setup_test_running(): assert is_doctest_running() == True
    """
    # this is used in our tests when we test cli-commands
    if os.getenv('PYTEST_IS_RUNNING'):
        return True

    for argv in sys.argv:
        if is_doctest_in_arg_string(argv):
            return True
    return False


def is_setup_test_running() -> bool:
    """if 'setup.py test' was launched"""
    for arg_string in sys.argv:
        if "setup.py" in arg_string:
            return True
    return False


def is_doctest_in_arg_string(arg_string: str) -> bool:
    """
    >>> assert is_doctest_in_arg_string('test') == False
    >>> assert is_doctest_in_arg_string('test/docrunner.py::::test')
    >>> assert is_doctest_in_arg_string('test/pytest.py::::test')
    """
    arg_string = arg_string.replace("\\", "/")
    if (
        ("docrunner.py" in arg_string)
        or ("pytest.py" in arg_string)
        or ("/pytest/__main__.py" in arg_string)
    ):
        return True
    else:
        return False


def add_path_to_syspath() -> None:
    """
    >>> add_path_to_syspath()
    """
    path_to_append = pathlib.Path(__file__).resolve().parent
    sys_paths_resolved = [pathlib.Path(path).resolve() for path in sys.path]
    if path_to_append not in sys_paths_resolved:
        sys.path.append(str(path_to_append))

if is_doctest_running():
    """
    we need to add the path to syspath for pytest and doctest
    """
    add_path_to_syspath()
