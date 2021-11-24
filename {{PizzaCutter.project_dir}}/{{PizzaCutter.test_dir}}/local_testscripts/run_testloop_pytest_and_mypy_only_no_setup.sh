#!/bin/bash
own_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" || exit && pwd -P )" # this gives the full path, even for sourced scripts

# shellcheck disable=SC2050
if [[ "{{PizzaCutter.True}}" != "True" ]]; then
    echo "exit - ${BASH_SOURCE[0]} is not configured by PizzaCutter"
    exit 0
fi

# shellcheck disable=SC1090
source "${own_dir}/lib_bash_functions.sh"
project_root_dir="${project_root_dir}"
DO_FLAKE8_TESTS="{{PizzaCutter.flake8_do_tests_in_local_testscript}}"
DO_MYPY_TESTS="{{PizzaCutter.testscript.do_mypy_tests}}"
DO_PYTEST="{{PizzaCutter.pytest_do_in_local_testscript}}"
DO_BLACK="{{PizzaCutter.auto_black_files}}"
# cleanup on cntrl-c
trap cleanup EXIT

# install dependencies
install_dependencies

function pytest_loop {
    while true; do
        banner "Project Root Dir: ${project_root_dir}"
        cleanup

        if [ "${DO_BLACK}" == "True" ]; then
          if ! run_black; then continue; fi
        fi

        # we prefer to run tests on its own, not within pytest, due to shaky and outdated pytest plugins
        if [ "${DO_FLAKE8_TESTS}" == "True" ]; then
          if ! run_flake8_tests; then continue; fi
        fi

        if [ "${DO_PYTEST}" == "True" ]; then
            if ! run_pytest --disable-warnings; then continue; fi
        fi

        # we prefer to run tests on its own, not within pytest, due to shaky and outdated pytest plugins
        if [ "${DO_MYPY_TESTS}" == "True" ]; then
            if ! run_mypy_tests; then continue; fi
        fi

        # if ! install_pip_requirements_venv; then continue; fi
        # if ! setup_test_venv; then continue; fi
        # if ! setup_install_venv; then continue; fi
        if ! test_commandline_interface_venv; then continue; fi

        banner "ALL TESTS PASSED for ${project_root_dir}"
        banner "ALL TESTS PASSED for ${project_root_dir}"
        banner "ALL TESTS PASSED for ${project_root_dir}"
        sleep 5
    done

}

# upgrade_pytest
# upgrade_mypy
pytest_loop
