# stdlib
import datetime
import logging
import pathlib
import subprocess
import sys
from typing import List, Optional

import lib_log_utils
from pizzacutter import PizzaCutterConfigBase
from pizzacutter import find_version_number_in_file

logger = logging.getLogger()
FORMAT = '%(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT)
logger.level = logging.INFO


class TravisLinuxTestMatrix(object):
    def __init__(self, arch: str,
                 python_version: str,
                 deploy_sdist: bool,
                 deploy_wheel: bool,
                 build_test: bool,
                 only_on_tagged_builds: bool,
                 build_docs: bool,
                 mypy_test: bool,
                 do_setup_install: bool,
                 do_setup_install_test: bool,
                 do_cli_test: bool
                 ):
        self.arch = arch
        self.python_version = python_version
        self.deploy_sdist = deploy_sdist
        self.deploy_wheel = deploy_wheel
        self.build_test = build_test
        self.only_on_tagged_builds = only_on_tagged_builds
        self.build_docs = build_docs
        self.mypy_test = mypy_test
        self.do_setup_install = do_setup_install
        self.do_setup_install_test = do_setup_install_test
        self.do_cli_test = do_cli_test


class PizzaCutterConfig(PizzaCutterConfigBase):
    def __init__(self,
                 pizza_cutter_path_conf_file: pathlib.Path = pathlib.Path(__file__).resolve(),
                 pizza_cutter_path_template_dir: Optional[pathlib.Path] = None,
                 pizza_cutter_path_target_dir: Optional[pathlib.Path] = None):

        if pizza_cutter_path_template_dir is None:
            pizza_cutter_path_template_dir = pathlib.Path(__file__).parent.resolve()

        super().__init__(pizza_cutter_path_conf_file, pizza_cutter_path_template_dir, pizza_cutter_path_target_dir)

# ##############################################################################################################################################################
# Pizza Cutter Configuration, can be override by cli
# ##############################################################################################################################################################

        # allow overwriting files in the project folder - this we need set to True in order to update projects
        self.pizza_cutter_allow_overwrite = True
        # if it is allowed to drop files outside of the project folder - this we set default to false,
        # but can be useful to drop files on the desktop, /etc, and so on
        self.pizza_cutter_allow_outside_write = False
        self.pizza_cutter_dry_run = False
        self.pizza_cutter_quiet = False

# ##############################################################################################################################################################
# Project Configuration - some lists that should only defined in the root configuration
# append or remove from that lists as needed !
# ##############################################################################################################################################################

        # ### requirements_test.txt Settings
        self.requirements_test: List[str] = list()


# ##############################################################################################################################################################
# Project Configuration - single point for all configuration of the project
# ##############################################################################################################################################################

        # ### Project Settings
        # the name of the project, for instance for the travis repo slug
        self.project_name = 'pct_python_default_test'
        # the project directory name (under the PizzaCutter Target folder)
        self.project_dir = self.project_name
        # the name of the package - usually it is used for cli command, package directory, etc
        self.package_name = 'pct_python_default_test'
        # a short description of the Package - especially if You deploy on PyPi !
        self.short_description = 'a pizzacutter default test project, crated with PizzaCutter and the PizzaCutter default python template'

        # self.version = '0.1.0'
        # this will be detected automatically from CHANGES.rst:
        self.version = find_version_number_in_file(pizza_cutter_path_target_dir / self.project_dir / 'CHANGES.rst')

        self.author = 'put Your Name here'
        self.author_email = 'some_email_address@gmail.com'
        self.github_account = 'your_github_account'
        # if the package is type annotated
        # in that case the file py.typed will be automatically created
        # "py.typed" and "*.pyi" will be included into setup_included_files
        # setup.py zip_safe is set to False
        self.is_typed_package = False

        # ### PyPi settings
        # if it is a PyPi Package, tagged Builds will be uploaded to PyPi by travis.yml
        # and we show the PyPi badge in README.rst
        self.is_pypi_package = False
        self.pypi_account = 'your_pypi_account'

        # additional pythonpaths to pass to the run_testloop.sh (lib_bash_functions.sh)
        self.testscript_additional_pythonpaths: List[str] = list()          # only append or delete from this list in inherited configs
        # for a list of codestyle options see : https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes

        # common excludes - usually excluded directories for different tools
        self.common_excludes: List[str] = ['.git', '__pycache__', 'build', 'dist', '.eggs', '.hg',
                                           '.mypy_cache', '.nox', '.tox', '.venv', '_build', 'buck-out']

        # #########################################################
        # ### pytest settings
        # #########################################################
        # those settings apply to local testscript
        self.pytest_do_travis = True
        self.pytest_do_gha = True
        self.pytest_do_local_testscript = True
        self.pytest_additional_args: List[str] = list()
        self.pytest_collect_ignores: List[str] = list()

        # #########################################################
        # ### flake8 settings
        # #########################################################
        self.requirements_test.append('flake8')
        self.flake8_do_tests_in_local_testscript = True
        self.flake8_do_tests_in_travis = True
        self.flake8_do_tests_in_gha = True
        # W503 and E203 are disabled for black, see : https://black.readthedocs.io/en/stable/the_black_code_style.html
        # F401, unused imports
        self.flake8_ignores: List[str] = ['E123', 'E203', 'E402', 'F401', 'F403', 'F405', 'W503']
        self.flake8_max_line_length: int = 88
        self.flake8_max_complexity: int = 10
        self.flake8_exclude: List[str] = self.common_excludes

        # #########################################################
        # ### black settings
        # #########################################################
        self.black_auto_in_local_testscript: bool = True
        self.black_show_badge: bool = self.black_auto_in_local_testscript
        self.requirements_test.append('black ; platform_python_implementation != "PyPy"')
        self.requirements_test.append('black==19.3b0 ; platform_python_implementation == "PyPy"')
        self.black_line_length: int = 88
        # put the lowest version in use here, so it will be compatible with later versions
        self.black_target_versions: List[str] = ['py36']
        self.black_include_regexp: str = r'\.pyi?$'
        self.black_exclude_regexp: str = r'/(\.eggs|\.git|\.hg|\.mypy_cache|\.nox|\.tox|\.venv|_build|buck-out|build|dist)/'

        # #########################################################
        # ### mypy settings
        # #########################################################

        self.mypy_strict_options: List[str] = ['--strict', '--warn-unused-ignores', '--implicit-reexport', '--follow-imports=silent',
                                               '--install-types', '--non-interactive']
        self.mypy_strict_options_follow_imports: List[str] = ['--strict', '--no-warn-unused-ignores', '--implicit-reexport', '--follow-imports=normal',
                                                              '--ignore-missing-imports', '--install-types', '--non-interactive']

        self.mypy_do_tests_in_local_testscript = True
        self.mypy_do_tests_in_travis = True
        self.mypy_do_tests_in_gha = True
        self.mypy_options_testscript: List[str] = self.mypy_strict_options_follow_imports
        self.mypy_options_travis: List[str] = self.mypy_strict_options_follow_imports
        self.mypy_options_gha: List[str] = self.mypy_strict_options_follow_imports

        # testscript_additional_mypy_paths:
        # additional project directories mypy needs to find
        # usually empty, unless You reference to typed packages locally, with local stub files or type definitions.
        # You must not point to directories with __init__.py in it, but to the directory above the package
        # in order mypy can find the import.
        # Module A:
        # import package_b
        # If You have for instance .../projects/project_b/package_b/__init__.py
        # You need to point to .../projects/project_b that mypy can import package_b
        # self.testscript_additional_mypy_dirs: List[pathlib.Path] = []
        # only append or delete from this list in inherited configs
        self.testscript_additional_mypy_paths: List[pathlib.Path] = list()

        # You dont have to add those directories one by one - You can automatically add
        # all immediate subdirectories dynamically in the testscript
        # so You dont need to reveal all your directories if You upload the project on github
        # self.testscript_additional_mypy_root_paths: List[pathlib.Path] = list()
        # only append or delete from this list in inherited configs
        self.testscript_additional_mypy_root_paths: List[pathlib.Path] = list()

        # #########################################################
        # ### coverage settings (coverage depends on pytest)
        # #########################################################
        # to upload code climate code coverage, You need to create the secret CC_TEST_REPORTER_ID
        self.coverage_do_travis = True
        self.coverage_do_gha = True
        self.coverage_do_local_testscript = True

        self.coverage_upload_codecov = True
        self.coverage_upload_code_climate = True

        self.do_code_coverage_code_climate = True
        self.do_code_coverage_codecov = True

        # #########################################################
        # ### Travis (and Github actions) settings
        # #########################################################
        # ### Github Tests
        self.add_github_actions = True

        # Travis Linux Version 'bionic', 'xenial', 'trusty', 'precise'
        self.travis_linux_version = 'bionic'
        self.travis_linux_tests = True
        self.gha_linux_tests = True
        self.travis_osx_tests = True
        self.gha_osx_tests = True
        self.travis_windows_tests = True
        self.gha_windows_tests = True
        self.travis_wine_tests = False
        self.gha_wine_tests = False

        # ### TRAVIS windows Test Matrix
        self.travis_windows_matrix_deploy_sdist = False
        self.travis_windows_matrix_deploy_wheel = False
        self.travis_windows_matrix_build_test = False
        self.travis_windows_matrix_only_on_tagged_builds = False
        self.travis_windows_matrix_build_docs = False
        self.travis_windows_matrix_mypy_test = True

        # ### GHA windows Test Matrix
        self.gha_windows_matrix_deploy_sdist = False
        self.gha_windows_matrix_deploy_wheel = False
        self.gha_windows_matrix_build_test = False
        self.gha_windows_matrix_only_on_tagged_builds = False
        self.gha_windows_matrix_build_docs = False
        self.gha_windows_matrix_mypy_test = True
        self.gha_windows_matrix_setup_install = True
        self.gha_windows_matrix_setup_install_test = True
        self.gha_windows_matrix_cli_test = True

        # ### TRAVIS osx Test Matrix
        self.travis_osx_matrix_deploy_sdist = False
        self.travis_osx_matrix_deploy_wheel = False
        self.travis_osx_matrix_build_test = True
        self.travis_osx_matrix_only_on_tagged_builds = False
        self.travis_osx_matrix_build_docs = False
        self.travis_osx_matrix_mypy_test = True

        # ### GHA osx Test Matrix
        self.gha_osx_matrix_deploy_sdist = True
        self.gha_osx_matrix_deploy_wheel = True
        self.gha_osx_matrix_build_test = True
        self.gha_osx_matrix_only_on_tagged_builds = False
        self.gha_osx_matrix_build_docs = False
        self.gha_osx_matrix_mypy_test = True
        self.gha_osx_matrix_setup_install = True
        self.gha_osx_matrix_setup_install_test = True
        self.gha_osx_matrix_cli_test = True

        # ### TRAVIS Linux Test Matrix
        self.travis_linux_test_matrix: List[TravisLinuxTestMatrix] = list()
        self.travis_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.6', build_test=True, mypy_test=True,
                                                                   deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=False,
                                                                   do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.travis_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.7', build_test=True, mypy_test=True,
                                                                   deploy_sdist=True, deploy_wheel=False, only_on_tagged_builds=False, build_docs=False,
                                                                   do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.travis_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.8', build_test=True, mypy_test=True,
                                                                   deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=False,
                                                                   do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.travis_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.9', build_test=True, mypy_test=True,
                                                                   deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=True,
                                                                   do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.travis_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.9-dev', build_test=True, mypy_test=True,
                                                                   deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=False,
                                                                   do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.travis_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='pypy3', build_test=True, mypy_test=False,
                                                                   deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=False,
                                                                   do_setup_install=True, do_setup_install_test=False, do_cli_test=True))

        self.travis_linux_test_matrix.append(TravisLinuxTestMatrix(arch='ppc64le', python_version='3.9', build_test=True, mypy_test=True,
                                                                   deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=True, build_docs=False,
                                                                   do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.travis_linux_test_matrix.append(TravisLinuxTestMatrix(arch='s390x', python_version='3.9', build_test=True, mypy_test=True,
                                                                   deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=True, build_docs=False,
                                                                   do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.travis_linux_test_matrix.append(TravisLinuxTestMatrix(arch='arm64', python_version='3.9', build_test=True, mypy_test=True,
                                                                   deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=True, build_docs=False,
                                                                   do_setup_install=True, do_setup_install_test=False, do_cli_test=True))

        # ### Github Actions Linux Test Matrix
        self.gha_linux_test_matrix: List[TravisLinuxTestMatrix] = list()
        self.gha_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.6', build_test=True, mypy_test=True,
                                                                deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=False,
                                                                do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.gha_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.7', build_test=True, mypy_test=True,
                                                                deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=False,
                                                                do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.gha_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.8', build_test=True, mypy_test=True,
                                                                deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=False,
                                                                do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.gha_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.9', build_test=True, mypy_test=True,
                                                                deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=False,
                                                                do_setup_install=True, do_setup_install_test=False, do_cli_test=True))
        self.gha_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='3.10.0', build_test=True, mypy_test=True,
                                                                deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=True,
                                                                do_setup_install=True, do_setup_install_test=True, do_cli_test=True))
        self.gha_linux_test_matrix.append(TravisLinuxTestMatrix(arch='amd64', python_version='pypy-3.8', build_test=True, mypy_test=False,
                                                                deploy_sdist=True, deploy_wheel=True, only_on_tagged_builds=False, build_docs=False,
                                                                do_setup_install=True, do_setup_install_test=False, do_cli_test=True))

        # ### .docs Settings
        # if to show badge for jupyter
        # create a new jupyter binder at https://mybinder.org/
        # and save it under the package name in the project folder
        self.docs_badges_with_jupiter = False
        # I would suggest '100%', 'good', 'some', 'progressing'
        self.docs_code_coverage_bragging = '100%'
        # valid choices for CI Badge : 'travis' or 'gha'
        self.docs_show_which_ci_badge: str = 'gha'

        # ### requirements_test.txt Settings
        # add here the requirements which will be needed for local or travis testing
        self.requirements_test.append('coloredlogs')
        self.requirements_test.append('pytest')
        self.requirements_test.append('pytest-runner')

        # ### setup.py Settings
        # include additional package data files here !!!
        self.setup_included_files: List[str] = list()
        # included_files.append('some_text_file.txt')
        # minimal python version required - also used in .docs
        self.setup_minimal_python_version_required = '3.6.0'
        # if can run from a zip file - see : https://setuptools.readthedocs.io/en/latest/setuptools.html#setting-the-zip-safe-flag
        self.setup_zip_safe = False

        self.setup_classifiers = ['Development Status :: 5 - Production/Stable',
                                  'Intended Audience :: Developers',
                                  'License :: OSI Approved :: MIT License',
                                  'Natural Language :: English',
                                  'Operating System :: OS Independent',
                                  'Programming Language :: Python',
                                  'Programming Language :: Python :: 3.6',
                                  'Programming Language :: Python :: 3.7',
                                  'Programming Language :: Python :: 3.8',
                                  'Programming Language :: Python :: pypy3',
                                  'Topic :: Software Development :: Libraries :: Python Modules']

        self.set_defaults()
        self.set_patterns()

    # ######################################################################################################################################################
    # DEFAULT SETTINGS - no need to change usually, but can be adopted
    # ######################################################################################################################################################
    def set_defaults(self):
        self.travis_secrets: List[str] = list()

        # the directory for the documentation
        self.docs_dir = '.docs'

        # the shell command which will be registered
        self.shell_command = self.package_name

        # the package directory under the project directory
        self.package_dir = self.package_name
        # the main module in package dir - will be imported into the cli_module
        self.main_module = self.package_name
        # the module where the entry point cli_method resides
        self.cli_module = self.package_name + '_cli'
        # the cli method to were the cli points
        self.cli_method = 'cli_main'
        # the title that is used for __init__.py __title__ and cli command INFO
        self.init_config_title = self.short_description
        # the name that is used for __init__.py __name__ and cli command INFO
        self.init_config_name = self.package_name
        # the path of the package dir
        self.path_package_dir = self.pizza_cutter_path_target_dir / self.project_dir / self.package_dir
        self.path_project_dir = self.pizza_cutter_path_target_dir / self.project_dir

        if self.flake8_do_tests_in_local_testscript or self.flake8_do_tests_in_travis or self.flake8_do_tests_in_gha:
            self.requirements_test.append('flake8')
        else:
            self.requirements_test.remove('flake8')

        if self.mypy_options_testscript or self.mypy_do_tests_in_travis or self.mypy_do_tests_in_gha:
            self.requirements_test.append('mypy ; platform_python_implementation != "PyPy"')
        else:
            self.requirements_test.remove('mypy ; platform_python_implementation != "PyPy"')

        if self.coverage_do_travis or self.coverage_do_local_testscript or self.coverage_do_gha:
            self.requirements_test.append('pytest-cov')
            self.requirements_test.append('coverage')
        else:
            self.requirements_test.remove('pytest-cov')
            self.requirements_test.remove('coverage')

        if self.coverage_upload_codecov:
            self.requirements_test.append('codecov')
        else:
            self.requirements_test.remove('codecov')

        if self.pytest_do_local_testscript or self.pytest_do_local_testscript:
            self.requirements_test.append('pytest')
            self.requirements_test.append('pytest-runner')
        else:
            self.requirements_test.remove('pytest')
            self.requirements_test.append('pytest-runner')

    # ##########################################################################################################################################################
    # replacement patterns
    # ##########################################################################################################################################################
    def set_patterns(self):
        """
        replacement patterns can be string, or pathlib.Path Objects - the pathlib Objects can be absolute or relative
        if You chain such pathlib Objects in template files or directories,, the final destination of the file might be not were You expected.
        since You might pass relative or absolute paths to the PizzaCutter CLI Application, You should be careful
        about the resulting paths, especially if You pass absolute paths.

        beware of differences in Linux and Windows : on Windows pathlib.Path('/test') is relative, on Linux it is absolute !
        best practice is to use relative paths in the form pathlib.Path('./test')

        with great flexibility there comes big responsibility. You should test Your Pizzacutter conf_files with absolute and relative Paths

        for the project path, and check carefully the result. We might disallow absolute paths in the future, or only enable it with a flag,
        not to allow dangerous Pizzacutter conf_files to overwrite system files.

        in general, if not really needed on purpose, we would suggest to use only string replacements in directory- and filenames.
        on the other hand, this feature can be very useful, in order t drop files to the user desktop,
        user home, windows appdir, etc... OUTSIDE of the Project Path given

        path replacement patterns are also valid in text files
        in that case the pattern will be replaced with the content of that file (if found)
        if the file is not found, or not readable, the string of the path will be filled in. (with a warning)
        You can even include Files from outside the template Folder, or from the Project Folder itself.

        Those replacements will be done AFTER the template Files are copied to the target Project, to make sure that even
        replacements from the target project file work properly.

        this can be useful for situations like:
        /template_folder/my_special_configuration{{PizzaCutter.option.no_overwrite}}.txt                          # template for the special configuration
        /template_folder/some_file.txt        # that file includes /project_folder/my_special_configuration.txt
        in that case, /project_folder/some_file.txt will include /project_folder/my_special_configuration.txt correctly,
        even if the project is just created.

        chaining of only relative Paths :
        {{PizzaCutter.relative_path_object1}} = pathlib.Path('test1/test2')   # relative path
        {{PizzaCutter.relative_path_object2}} = pathlib.Path('test3/test4')   # relative path
        .../template_directory/{{PizzaCutter.relative_path_object1}}/{{PizzaCutter.relative_path_object2}}/test.txt  will work as expected. and resolve to:
        .../template_directory/test1/test2/test3/test4/test.txt --> .../project_directory/test1/test2/test3/test4/test.txt

        chaining of Absolute and Relative Paths :
        {{PizzaCutter.absolute_path_object1}} = pathlib.Path('/test1/test2')  # absolute Path
        {{PizzaCutter.relative_path_object2}} = pathlib.Path('test3/test4')   # relative path
        .../template_directory/{{PizzaCutter.absolute_path_object1}}/{{PizzaCutter.relative_path_object2}}/test.txt  will work as expected. and resolve to:
        /test1/test2/test3/test4/test.txt
        by that way You might even write configuration files into /usr/etc or similar (depending on Your rights)!

        unexpected Result when chaining Absolute and Relative Paths in the wrong order :
        {{PizzaCutter.relative_path_object1}} = pathlib.Path('test1/test2')   # relative Path
        {{PizzaCutter.absolute_path_object2}} = pathlib.Path('/test3/test4')  # absolute path
        .../template_directory/{{PizzaCutter.relative_path_object1}}/{{PizzaCutter.absolute_path_object2}}/test.txt will work unexpected and resolve to:
        /test3/test4/test.txt
        by that way You might even write configuration files into /usr/etc or similar (depending on Your rights)!

        ######################################################################################################################################################

        remember - the directory structure in the template dont have to be the same as in the target project -
        '{{PizzaCutter.path_package_dir}}' will resolve to the directory given in the variable path_package_dir, because its pathlib.Path type.
        if You pass a string type, the directory in the project will be relative to the position in the template - as You prefer !

        """

        self.url = f'https://github.com/{self.github_account}/{self.project_name}'
        self.github_master = f'git+https://github.com/{self.github_account}/{self.project_name}.git'
        self.travis_repo_slug = self.github_account + '/' + self.project_name
        # we ned to have a function main_commandline in module module_name - see examples
        self.setup_entry_points = {'console_scripts': [f'{self.shell_command} = {self.package_dir}.{self.cli_module}:{self.cli_method}']}

        if self.is_typed_package:
            self.setup_included_files.append('py.typed')
            self.setup_included_files.append('*.pyi')
            # we need to add __init__.pyi explicitly or it will not be included
            self.setup_included_files.append('__init__.pyi')
            # setup_zip_safe needs to be false for a typed project
            # noinspection PyRedeclaration
            self.setup_zip_safe = False
        else:
            # we need to remove otherwise !
            remove_from_list(self.setup_included_files, 'py.typed')
            remove_from_list(self.setup_included_files, '*.pyi')
            remove_from_list(self.setup_included_files, '__init__.pyi')

        self.setup_package_data = {self.package_name: self.setup_included_files}

        self.pizza_cutter_patterns['{{PizzaCutter.project_name}}'] = self.project_name
        self.pizza_cutter_patterns['{{PizzaCutter.project_dir}}'] = self.project_dir
        self.pizza_cutter_patterns['{{PizzaCutter.package_name}}'] = self.package_name
        self.pizza_cutter_patterns['{{PizzaCutter.path.package_dir}}'] = self.path_package_dir
        self.pizza_cutter_patterns['{{PizzaCutter.short_description}}'] = self.short_description
        self.pizza_cutter_patterns['{{PizzaCutter.repository_slug}}'] = self.travis_repo_slug
        self.pizza_cutter_patterns['{{PizzaCutter.repository}}'] = self.project_name
        self.pizza_cutter_patterns['{{PizzaCutter.double_underline_repository}}'] = '=' * len(self.project_name)
        # on some places You need to put the repo name in dashes on PyPi
        self.pizza_cutter_patterns['{{PizzaCutter.repository_dashed}}'] = self.project_name.replace('_', '-')
        self.pizza_cutter_patterns['{{PizzaCutter.version}}'] = self.version
        self.pizza_cutter_patterns['{{PizzaCutter.title}}'] = self.init_config_title
        self.pizza_cutter_patterns['{{PizzaCutter.name}}'] = self.init_config_name
        self.pizza_cutter_patterns['{{PizzaCutter.url}}'] = self.url
        self.pizza_cutter_patterns['{{PizzaCutter.author}}'] = self.author
        self.pizza_cutter_patterns['{{PizzaCutter.author_email}}'] = self.author_email
        self.pizza_cutter_patterns['{{PizzaCutter.shell_command}}'] = self.shell_command
        self.pizza_cutter_patterns['{{PizzaCutter.pypi_account}}'] = self.pypi_account
        self.pizza_cutter_patterns['{{PizzaCutter.travis_repo_slug}}'] = self.travis_repo_slug
        self.pizza_cutter_patterns['{{PizzaCutter.github_master}}'] = self.github_master

        # here passed as string - used in .travis.yml
        self.pizza_cutter_patterns['{{PizzaCutter.package_dir}}'] = self.package_dir
        # we add the .py extension here in that case - so that it is not a .py file in the template folder.
        # that is because otherwise our IDE will show it as a faulty .py file because of the replace markers in the import statement
        self.pizza_cutter_patterns['{{PizzaCutter.main_module}}'] = self.main_module
        self.pizza_cutter_patterns['{{PizzaCutter.main_module_filename}}'] = self.main_module
        self.pizza_cutter_patterns['{{PizzaCutter.cli_module}}'] = self.cli_module
        self.pizza_cutter_patterns['{{PizzaCutter.cli_module_filename}}'] = self.cli_module
        self.pizza_cutter_patterns['{{PizzaCutter.cli_method}}'] = self.cli_method
        # here we pass a path as string - so it will resolve from <template_dir>.{{PizzaCutter.docs_dir}} to <path_target_project_folder>/.docs
        # used in .rotekignore
        self.pizza_cutter_patterns['{{PizzaCutter.docs_dir}}'] = self.docs_dir
        # used in .rotekignore
        self.pizza_cutter_patterns['{{PizzaCutter.test_dir}}'] = 'tests'
        # used in .coveragerc, just in case You keep the conf file in the project directory
        self.pizza_cutter_patterns['{{PizzaCutter.conf_file_name}}'] = self.pizza_cutter_path_conf_file.name
        # used in Licence
        self.pizza_cutter_patterns['{{PizzaCutter.current_year}}'] = str(datetime.datetime.now().year)
        self.pizza_cutter_patterns['{{PizzaCutter.date}}'] = datetime.datetime.today().strftime('%Y-%m-%d')

        if self.docs_badges_with_jupiter:
            self.pizza_cutter_patterns['{{PizzaCutter.|jupyter| }}'] = '|jupyter| '
            self.pizza_cutter_patterns['{{PizzaCutter.try_in_jupyter}}'] = '.. include:: ./try_in_jupyter.rst'
            self.pizza_cutter_patterns['{{PizzaCutter.index_entry_jupyter}}'] = '- `Try it Online`_'
        else:
            self.pizza_cutter_patterns['{{PizzaCutter.|jupyter| }}'] = ''
            self.pizza_cutter_patterns['{{PizzaCutter.try_in_jupyter}}'] = ''
            self.pizza_cutter_patterns['{{PizzaCutter.index_entry_jupyter}}'] = ''

        if self.is_pypi_package:
            self.pizza_cutter_patterns['{{PizzaCutter.|pypi|}}'] = '|pypi|'
        else:
            self.pizza_cutter_patterns['{{PizzaCutter.|pypi|}}'] = ''

        self.setup_docs_test_info()
        self.setup_docs_installation_pypi()
        self.setup_docs_python_test_info()
        self.setup_testscripts()
        self.setup_travis()
        self.setup_travis_secrets()
        self.setup_travis_linux_tests()
        self.setup_gha_linux_tests()
        self.setup_travis_windows_tests()
        self.setup_travis_osx_tests()
        self.setup_requirements_test()
        self.setup_setup_py()
        self.setup_coverage()
        self.setup_flake8()
        self.setup_mypy()
        self.setup_black()
        self.setup_pytest()

    # ############################################################################
    # pytest settings
    # ############################################################################
    def setup_pytest(self):
        additional_args = sorted(list(set(self.pytest_additional_args)))
        collect_ignores = sorted(list(set(self.pytest_collect_ignores)))
        self.pizza_cutter_patterns['{{PizzaCutter.pytest.additional_args}}'] = str(additional_args)
        self.pizza_cutter_patterns['{{PizzaCutter.pytest.collect_ignore}}'] = str(collect_ignores)
        self.pizza_cutter_patterns['{{PizzaCutter.pytest_do_in_local_testscript}}'] = str(self.pytest_do_local_testscript)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.pytest_do_tests}}'] = str(self.pytest_do_travis)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.pytest_do_tests}}'] = str(self.pytest_do_gha)

    # ############################################################################
    # requirements_test.txt settings
    # ############################################################################
    def setup_requirements_test(self):
        self.requirements_test = sorted(list(set(self.requirements_test)))
        self.pizza_cutter_patterns['# {{PizzaCutter.requirements_test}}'] = '\n'.join(self.requirements_test)

    # ############################################################################
    # flake8 settings
    # ############################################################################
    def setup_flake8(self):
        self.pizza_cutter_patterns['{{PizzaCutter.flake8_do_tests_in_local_testscript}}'] = str(self.flake8_do_tests_in_local_testscript)
        self.pizza_cutter_patterns['{{PizzaCutter.flake8_do_tests_in_travis}}'] = str(self.flake8_do_tests_in_travis)
        self.pizza_cutter_patterns['{{PizzaCutter.flake8_do_tests_in_gha}}'] = str(self.flake8_do_tests_in_gha)
        self.pizza_cutter_patterns['{{PizzaCutter.flake8_ignores}}'] = ', '.join(self.flake8_ignores)
        self.pizza_cutter_patterns['{{PizzaCutter.flake8_max_line_length}}'] = str(self.flake8_max_line_length)
        self.pizza_cutter_patterns['{{PizzaCutter.flake8_max_complexity}}'] = str(self.flake8_max_complexity)
        self.pizza_cutter_patterns['{{PizzaCutter.flake8_exclude}}'] = ', '.join(self.flake8_exclude)

    # ############################################################################
    # flake8 settings
    # ############################################################################
    def setup_coverage(self):
        self.pizza_cutter_patterns['{{PizzaCutter.travis.do_coverage}}'] = str(self.coverage_do_travis)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.do_coverage}}'] = str(self.coverage_do_gha)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.do_coverage_upload_codecov}}'] = str(self.coverage_upload_codecov)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.do_coverage_upload_codecov}}'] = str(self.coverage_upload_codecov)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.do_coverage_upload_code_climate}}'] = str(self.coverage_upload_code_climate)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.do_coverage_upload_code_climate}}'] = str(self.coverage_upload_code_climate)
        self.pizza_cutter_patterns['{{PizzaCutter.testscript.do_coverage}}'] = str(self.coverage_do_local_testscript)

        if self.coverage_do_local_testscript:
            # coverage_option = '--cov={package_name} --cov-config=.coveragerc'.format(package_name=self.package_name)
            # since not all modules were discovered, we use the directory - this seems to work
            # --cov-config=.coveragerc
            coverage_option = '--cov="${project_root_dir}" --cov-config=.coveragerc'
        else:
            coverage_option = ''
        self.pizza_cutter_patterns['{{PizzaCutter.testscript.pytest_coverage_option}}'] = coverage_option

        self.coverage_do_local_testscript = True

        self.coverage_upload_codecov = True
        self.coverage_upload_code_climate = True

        self.do_code_coverage_code_climate = True
        self.do_code_coverage_codecov = True

    # ############################################################################
    # mypy settings
    # ############################################################################
    def setup_mypy(self):
        self.pizza_cutter_patterns['{{PizzaCutter.travis.mypy_do_tests}}'] = str(self.mypy_do_tests_in_travis)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.mypy_do_tests}}'] = str(self.mypy_do_tests_in_gha)
        self.pizza_cutter_patterns['{{PizzaCutter.testscript.do_mypy_tests}}'] = str(self.mypy_do_tests_in_local_testscript)

        travis_mypy_options = sorted(list(set(self.mypy_options_travis)))
        gha_mypy_options = sorted(list(set(self.mypy_options_gha)))
        testscript_mypy_options = sorted(list(set(self.mypy_options_testscript)))
        self.pizza_cutter_patterns['{{PizzaCutter.travis.mypy_options}}'] = ' '.join(travis_mypy_options)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.mypy_options}}'] = ' '.join(gha_mypy_options)
        self.pizza_cutter_patterns['{{PizzaCutter.testscript.mypy_options}}'] = ' '.join(testscript_mypy_options)

    # ############################################################################
    # black settings
    # ############################################################################
    def setup_black(self):
        self.pizza_cutter_patterns['{{PizzaCutter.black_line_length}}'] = str(self.black_line_length)
        self.pizza_cutter_patterns['{{PizzaCutter.black_target_versions}}'] = str(self.black_target_versions)
        self.pizza_cutter_patterns['{{PizzaCutter.black_include_regexp}}'] = self.black_include_regexp
        self.pizza_cutter_patterns['{{PizzaCutter.black_exclude_regexp}}'] = self.black_exclude_regexp
        self.pizza_cutter_patterns['{{PizzaCutter.auto_black_files}}'] = str(self.black_auto_in_local_testscript)

        if self.black_show_badge:
            self.pizza_cutter_patterns['{{PizzaCutter.|black|}}'] = '|black|'
        else:
            self.pizza_cutter_patterns['{{PizzaCutter.|black|}}'] = ''

    # ############################################################################
    # setup.py settings
    # ############################################################################
    def setup_setup_py(self):
        self.pizza_cutter_patterns['{{PizzaCutter.setup_python_requires}}'] = '">={}"'.format(self.setup_minimal_python_version_required)
        self.pizza_cutter_patterns['{{PizzaCutter.setup_package_data}}'] = str(self.setup_package_data)
        self.pizza_cutter_patterns['{{PizzaCutter.setup_classifiers}}'] = str(self.setup_classifiers)
        self.pizza_cutter_patterns['{{PizzaCutter.setup_entry_points}}'] = str(self.setup_entry_points)
        self.pizza_cutter_patterns['{{PizzaCutter.setup_zip_safe}}'] = str(self.setup_zip_safe)

    # ############################################################################
    # .travis.yml settings
    # ############################################################################
    def setup_travis(self):
        self.pizza_cutter_patterns['{{PizzaCutter.travis.linux_version}}'] = self.travis_linux_version
        self.pizza_cutter_patterns['{{PizzaCutter.travis_windows_addon}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.travis_linux_addon}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.travis_pypy_addon}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.travis_osx_addon}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.travis_wine_addon}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.gha_windows_addon}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.gha_linux_addon}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.gha_pypy_addon}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.gha_osx_addon}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.gha_wine_addon}}'] = ''

        if self.travis_windows_tests:
            self.pizza_cutter_patterns['{{PizzaCutter.travis_windows_addon}}'] = \
                (self.pizza_cutter_path_template_dir /
                 '{{PizzaCutter.project_dir}}/travis_addons{{PizzaCutter.option.no_copy}}/travis_template_windows_addon.yml').read_text()

        if self.gha_windows_tests:
            self.pizza_cutter_patterns['{{PizzaCutter.gha_windows_addon}}'] = \
                (self.pizza_cutter_path_template_dir /
                 '{{PizzaCutter.project_dir}}/gha_addons{{PizzaCutter.option.no_copy}}/gha_template_windows_addon.yml').read_text()

        if self.travis_osx_tests:
            self.pizza_cutter_patterns['{{PizzaCutter.travis_osx_addon}}'] = \
                (self.pizza_cutter_path_template_dir /
                 '{{PizzaCutter.project_dir}}/travis_addons{{PizzaCutter.option.no_copy}}/travis_template_osx_addon.yml').read_text()

        if self.gha_osx_tests:
            self.pizza_cutter_patterns['{{PizzaCutter.gha_osx_addon}}'] = \
                (self.pizza_cutter_path_template_dir /
                 '{{PizzaCutter.project_dir}}/gha_addons{{PizzaCutter.option.no_copy}}/gha_template_osx_addon.yml').read_text()

        if self.travis_wine_tests:
            self.pizza_cutter_patterns['{{PizzaCutter.travis_wine_addon}}'] = \
                (self.pizza_cutter_path_template_dir /
                 '{{PizzaCutter.project_dir}}/travis_addons{{PizzaCutter.option.no_copy}}/travis_template_wine_addon.yml').read_text()

        if self.gha_wine_tests:
            self.pizza_cutter_patterns['{{PizzaCutter.gha_wine_addon}}'] = \
                (self.pizza_cutter_path_template_dir /
                 '{{PizzaCutter.project_dir}}/gha_addons{{PizzaCutter.option.no_copy}}/gha_template_wine_addon.yml').read_text()

        # travis rst_include (rebuild Readme File)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.rst_include_source}}'] = f'./{self.docs_dir}/README_template.rst'
        self.pizza_cutter_patterns['{{PizzaCutter.travis.rst_include_target}}'] = './README.rst'
        self.pizza_cutter_patterns['{{PizzaCutter.gha.rst_include_source}}'] = f'./{self.docs_dir}/README_template.rst'
        self.pizza_cutter_patterns['{{PizzaCutter.gha.rst_include_target}}'] = './README.rst'

    # ############################################################################
    # .travis.yml settings
    # ############################################################################
    def setup_travis_secrets(self) -> None:
        str_secure = '        - secure: {encrypted_secret}  # {comment}'
        path_secrets = self.path_project_dir / 'travis_secrets/secrets'

        self.pizza_cutter_patterns['{{PizzaCutter.travis.secrets}}'] = ''

        if not path_secrets.exists():
            return

        path_secret_files = path_secrets.glob('*.secret.txt')
        l_secrets: List[str] = list()
        for path_secret_file in path_secret_files:
            env_var_name = path_secret_file.stem
            encrypted_secret = path_secret_file.read_text().strip()
            str_secret = str_secure.format(encrypted_secret=encrypted_secret, comment=env_var_name)
            l_secrets.append(str_secret)
            self.pizza_cutter_patterns['{{PizzaCutter.travis.secrets}}'] = '\n'.join(l_secrets)
            if not self.project_name.startswith('pct_python_default_'):
                logger.info(f'Project {self.project_name}: set encrypted environment variable "{env_var_name}"')

    # ############################################################################
    # .travis Linux Matrix settings
    # ############################################################################
    def setup_travis_linux_tests(self) -> None:
        if not self.travis_linux_tests:
            self.pizza_cutter_patterns['{{PizzaCutter.travis.linux.tests}}'] = ''
        else:
            l_travis_linux_tests: List[str] = list()
            for matrix_item in self.travis_linux_test_matrix:
                arch = matrix_item.arch

                if matrix_item.only_on_tagged_builds:
                    condition = 'tag IS present'
                else:
                    condition = 'true'
                build_docs = matrix_item.build_docs
                deploy_sdist = matrix_item.deploy_sdist
                deploy_wheel = matrix_item.deploy_wheel
                build_test = matrix_item.build_test
                python_version = matrix_item.python_version
                mypy_test = matrix_item.mypy_test and self.mypy_do_tests_in_travis
                travis_linux_matrix_item = \
                    f"""
    - os: linux
      arch: "{arch}"
      if: {condition}
      language: python
      python: "{python_version}"
      before_install:
          - export BUILD_DOCS="{build_docs}"
          - export DEPLOY_SDIST="{deploy_sdist}"
          - export DEPLOY_WHEEL="{deploy_wheel}"
          - export BUILD_TEST="{build_test}"
          - export MYPY_DO_TESTS="{mypy_test}"
"""

                l_travis_linux_tests.append(travis_linux_matrix_item)
            self.pizza_cutter_patterns['{{PizzaCutter.travis.linux.tests}}'] = ''.join(l_travis_linux_tests)

    # ############################################################################
    # github_actions Linux Matrix settings
    # ############################################################################
    def setup_gha_linux_tests(self) -> None:
        if not self.gha_linux_tests:
            self.pizza_cutter_patterns['{{PizzaCutter.gha.linux.tests}}'] = ''
        else:
            l_gha_linux_tests: List[str] = list()
            for matrix_item in self.gha_linux_test_matrix:
                arch = matrix_item.arch

                if matrix_item.only_on_tagged_builds:
                    condition = 'tag IS present'
                else:
                    condition = 'true'
                build_docs = matrix_item.build_docs
                deploy_sdist = matrix_item.deploy_sdist
                deploy_wheel = matrix_item.deploy_wheel
                build_test = matrix_item.build_test
                python_version = matrix_item.python_version
                mypy_test = matrix_item.mypy_test and self.mypy_do_tests_in_gha
                do_setup_install = matrix_item.do_setup_install
                do_setup_install_test = matrix_item.do_setup_install_test
                do_cli_test = matrix_item.do_cli_test

                gha_linux_matrix_item = \
                    f"""
          - os: ubuntu-latest
            python-version: "{python_version}"
            env:
              BUILD_DOCS: "{build_docs}"
              DEPLOY_SDIST: "{deploy_sdist}"
              DEPLOY_WHEEL: "{deploy_wheel}"
              DEPLOY_TEST: "{build_test}"
              MYPY_DO_TESTS: "{mypy_test}"
              DO_SETUP_INSTALL: "{do_setup_install}"
              DO_SETUP_INSTALL_TEST: "{do_setup_install_test}"
              DO_CLI_TEST: "{do_cli_test}"
"""

                l_gha_linux_tests.append(gha_linux_matrix_item)

            self.pizza_cutter_patterns['{{PizzaCutter.gha.linux.tests}}'] = ''.join(l_gha_linux_tests)

    # ############################################################################
    # .travis Windows Matrix settings
    # ############################################################################
    def setup_travis_windows_tests(self) -> None:
        self.pizza_cutter_patterns['{{PizzaCutter.travis.windows.deploy_sdist}}'] = str(self.travis_windows_matrix_deploy_sdist)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.windows.deploy_wheel}}'] = str(self.travis_windows_matrix_deploy_wheel)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.windows.build_test}}'] = str(self.travis_windows_matrix_build_test)
        if self.travis_windows_matrix_only_on_tagged_builds:
            condition = 'tag IS present'
        else:
            condition = 'true'
        self.pizza_cutter_patterns['{{PizzaCutter.travis.windows.condition}}'] = condition
        self.pizza_cutter_patterns['{{PizzaCutter.travis.windows.build_docs}}'] = str(self.travis_windows_matrix_build_docs)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.windows.mypy_test}}'] = str(self.travis_windows_matrix_mypy_test and self.mypy_do_tests_in_travis)

        # GHA
        self.pizza_cutter_patterns['{{PizzaCutter.gha.windows.deploy_sdist}}'] = str(self.gha_windows_matrix_deploy_sdist)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.windows.deploy_wheel}}'] = str(self.gha_windows_matrix_deploy_wheel)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.windows.build_test}}'] = str(self.gha_windows_matrix_build_test)
        if self.gha_windows_matrix_only_on_tagged_builds:
            condition = 'tag IS present'
        else:
            condition = 'true'
        self.pizza_cutter_patterns['{{PizzaCutter.gha.windows.condition}}'] = condition
        self.pizza_cutter_patterns['{{PizzaCutter.gha.windows.build_docs}}'] = str(self.gha_windows_matrix_build_docs)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.windows.mypy_test}}'] = str(self.gha_windows_matrix_mypy_test and self.mypy_do_tests_in_gha)

        self.pizza_cutter_patterns['{{PizzaCutter.gha.windows.setup.py.install}}'] = str(self.gha_windows_matrix_setup_install)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.windows.setup.py.test}}'] = str(self.gha_windows_matrix_setup_install_test)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.windows.cli.test}}'] = str(self.gha_windows_matrix_cli_test)

    # ############################################################################
    # .travis Windows Matrix settings
    # ############################################################################
    def setup_travis_osx_tests(self) -> None:
        self.pizza_cutter_patterns['{{PizzaCutter.travis.osx.deploy_sdist}}'] = str(self.travis_osx_matrix_deploy_sdist)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.osx.deploy_wheel}}'] = str(self.travis_osx_matrix_deploy_wheel)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.osx.build_test}}'] = str(self.travis_osx_matrix_build_test)
        if self.travis_osx_matrix_only_on_tagged_builds:
            condition = 'tag IS present'
        else:
            condition = 'true'
        self.pizza_cutter_patterns['{{PizzaCutter.travis.osx.condition}}'] = condition
        self.pizza_cutter_patterns['{{PizzaCutter.travis.osx.build_docs}}'] = str(self.travis_osx_matrix_build_docs)
        self.pizza_cutter_patterns['{{PizzaCutter.travis.osx.mypy_test}}'] = str(self.travis_osx_matrix_mypy_test and self.mypy_do_tests_in_travis)

        self.pizza_cutter_patterns['{{PizzaCutter.gha.osx.deploy_sdist}}'] = str(self.gha_osx_matrix_deploy_sdist)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.osx.deploy_wheel}}'] = str(self.gha_osx_matrix_deploy_wheel)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.osx.build_test}}'] = str(self.gha_osx_matrix_build_test)
        if self.gha_osx_matrix_only_on_tagged_builds:
            condition = 'tag IS present'
        else:
            condition = 'true'
        self.pizza_cutter_patterns['{{PizzaCutter.gha.osx.condition}}'] = condition
        self.pizza_cutter_patterns['{{PizzaCutter.gha.osx.build_docs}}'] = str(self.gha_osx_matrix_build_docs)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.osx.mypy_test}}'] = str(self.gha_osx_matrix_mypy_test and self.mypy_do_tests_in_gha)

        self.pizza_cutter_patterns['{{PizzaCutter.gha.osx.setup.py.install}}'] = str(self.gha_osx_matrix_setup_install)
        self.pizza_cutter_patterns['{{PizzaCutter.gha.osx.setup.py.test}}'] = str(self.gha_osx_matrix_setup_install_test)

        self.pizza_cutter_patterns['{{PizzaCutter.gha.osx.cli.test}}'] = str(self.gha_osx_matrix_cli_test)

    # ############################################################################
    # test_dir/local_testscripts settings
    # ############################################################################
    def setup_testscripts(self):

        # set additional PYTHONPATH
        add_python_path_bash_command = 'export PYTHONPATH="$(python3 ./testing_tools.py append_directory_to_python_path "{python_path}")"'
        l_python_paths: List[str] = list()
        for python_path in self.testscript_additional_pythonpaths:
            if not pathlib.Path(python_path).is_dir():
                logger.warning(f'PYTHONPATH "{python_path}" does not exist, skipping')
            l_python_paths.append(add_python_path_bash_command.format(python_path=python_path))
        python_paths = '\n'.join(l_python_paths)
        self.pizza_cutter_patterns['# {{PizzaCutter.testscript.append_additional_python_paths}}'] = python_paths

        # set additional MYPYPATH
        add_mypy_path_bash_command = 'export MYPYPATH="$(python3 ./testing_tools.py append_directory_to_python_path "{mypy_path}")"'
        l_mypy_paths: List[str] = list()
        for mypy_path in self.testscript_additional_mypy_paths:
            if not mypy_path.is_dir():
                logger.warning(f'MYPYPATH "{mypy_path}" does not exist, skipping')
            l_mypy_paths.append(add_mypy_path_bash_command.format(mypy_path=mypy_path))
        mypy_paths = '\n'.join(l_mypy_paths)
        self.pizza_cutter_patterns['# {{PizzaCutter.testscript.append_additional_mypy_paths}}'] = mypy_paths

        # set additional MYPYPATH from a root directory - add all immediate subdirs as mypy path in the testscript
        add_mypy_root_path_bash_command = 'export MYPYPATH="$(python3 ./testing_tools.py append_immediate_subdirs_to_mypy_path "{mypy_root_path}")"'
        l_mypy_root_paths: List[str] = list()
        for mypy_root_path in self.testscript_additional_mypy_root_paths:
            if not mypy_root_path.is_dir():
                logger.warning(f'we can not add the immediate subdirs to MYPYPATH, because "{mypy_root_path}" does not exist, skipping')
            l_mypy_root_paths.append(add_mypy_root_path_bash_command.format(mypy_root_path=mypy_root_path))
        mypy_root_paths = '\n'.join(l_mypy_root_paths)
        self.pizza_cutter_patterns['# {{PizzaCutter.testscript.append_additional_mypy_paths_from_root_dir}}'] = mypy_root_paths

    # ############################################################################
    # docs - {{PizzaCutter.docs.python_test_info}} for .docs/tested_under.rst
    # ############################################################################
    def setup_docs_python_test_info(self) -> None:
        # supports python 3.6-3.8, pypy3 and possibly other dialects.
        # tested for python 3.6, 3.7, 3.8, 3.8-dev, pypy3
        def get_travis_linux_versions():
            linux_versions: List[str] = list()
            for travis_linux_test in self.travis_linux_test_matrix:
                if travis_linux_test.python_version not in linux_versions:
                    linux_versions.append(travis_linux_test.python_version)
            return linux_versions

        def get_travis_archs():
            archs: List[str] = list()
            for travis_linux_test in self.travis_linux_test_matrix:
                if travis_linux_test.arch not in archs:
                    archs.append(travis_linux_test.arch)
            return archs

        def get_gha_linux_versions():
            linux_versions: List[str] = list()
            for gha_linux_test in self.gha_linux_test_matrix:
                if gha_linux_test.python_version not in linux_versions:
                    linux_versions.append(gha_linux_test.python_version)
            return linux_versions

        def get_gha_archs():
            archs: List[str] = list()
            for gha_linux_test in self.gha_linux_test_matrix:
                if gha_linux_test.arch not in archs:
                    archs.append(gha_linux_test.arch)
            return archs

        str_python_test_info = ''
        if self.docs_show_which_ci_badge.lower() == 'travis':
            str_python_test_info = 'tested on linux "{travis_python_version}" with python {versions} - architectures: {architectures}'.format(
                travis_python_version=self.travis_linux_version,
                versions=', '.join(get_travis_linux_versions()),
                architectures=', '.join(get_travis_archs()),
                )
        elif self.docs_show_which_ci_badge.lower() == 'gha':
            str_python_test_info = 'tested on recent linux with python {versions} - architectures: {architectures}'.format(
                versions=', '.join(get_gha_linux_versions()),
                architectures=', '.join(get_gha_archs()),
                )
        else:
            lib_log_utils.log_warning(f'unsupported parameter self.docs_show_which_ci_badge: {self.docs_show_which_ci_badge}')

        self.pizza_cutter_patterns['{{PizzaCutter.docs.python_test_info}}'] = str_python_test_info
        self.pizza_cutter_patterns['{{PizzaCutter.docs.python_required}}'] = self.setup_minimal_python_version_required

    # ############################################################################
    # docs - {{PizzaCutter.docs.pypi_requirements}}, {{PizzaCutter.docs.include_installation_via_pypi}}
    # ############################################################################
    def setup_docs_installation_pypi(self):
        if self.is_pypi_package:
            doc_string = f'# for the latest Release on pypi:\n    {self.project_name}\n'
            self.pizza_cutter_patterns['{{PizzaCutter.docs.pypi_requirements}}'] = doc_string
            self.pizza_cutter_patterns['{{PizzaCutter.docs.include_installation_via_pypi}}'] = '.. include:: ./installation_via_pypi.rst'
        else:
            self.pizza_cutter_patterns['{{PizzaCutter.docs.pypi_requirements}}'] = ''
            self.pizza_cutter_patterns['{{PizzaCutter.docs.include_installation_via_pypi}}'] = ''

    # ############################################################################
    # docs - {{PizzaCutter.docs.test_info}} for .docs/tested_under.rst
    # ############################################################################
    def setup_docs_test_info(self):
        """
        creates the pattern {{PizzaCutter.docs.test_info}} for .docs/tested_under.rst

        `100% code coverage <https://codecov.io/gh/{{PizzaCutter.repository_slug}}>`_, codestyle checking, mypy static type checking,
        tested under `Linux, macOS, Windows and Wine <https://travis-ci.org/{{PizzaCutter.repository_slug}}>`_, automatic daily builds and monitoring

        """

        if self.coverage_upload_codecov:
            link_coverage = 'https://codecov.io/gh/{travis_repo_slug}'.format(travis_repo_slug=self.travis_repo_slug)
        else:
            link_coverage = 'https://codeclimate.com/github/{travis_repo_slug}/test_coverage'.format(travis_repo_slug=self.travis_repo_slug)

        if self.coverage_do_travis or self.coverage_do_local_testscript or self.coverage_do_gha:
            msg_code_coverage = '`{docs_code_coverage_bragging} code coverage <{link_coverage}>`_, '.format(
                docs_code_coverage_bragging=self.docs_code_coverage_bragging,
                link_coverage=link_coverage
                )
        else:
            msg_code_coverage = ''

        if self.flake8_do_tests_in_travis or self.flake8_do_tests_in_gha:
            msg_style_checking = 'flake8 style checking ,'
        else:
            msg_style_checking = ''

        if self.mypy_do_tests_in_travis or self.mypy_do_tests_in_gha:
            msg_mypy_tests = 'mypy static type checking ,'
        else:
            msg_mypy_tests = ''

        l_tested_under: List[str] = list()

        if self.travis_linux_tests:
            l_tested_under.append('Linux')

        if self.travis_osx_tests:
            l_tested_under.append('macOS')

        if self.travis_windows_tests or self.gha_windows_tests:
            l_tested_under.append('Windows')

        if self.travis_wine_tests or self.gha_wine_tests:
            l_tested_under.append('Wine')

        test_link = ''
        self.pizza_cutter_patterns['{{PizzaCutter.docs.build_badge}}'] = ''
        self.pizza_cutter_patterns['{{PizzaCutter.docs.build_badge_link}}'] = ''
        if self.docs_show_which_ci_badge == 'travis':
            test_link = f' <https://travis-ci.org/{self.travis_repo_slug}>`_, automatic daily builds and monitoring'
            self.pizza_cutter_patterns['{{PizzaCutter.docs.build_badge}}'] = '|build_badge| '
            self.pizza_cutter_patterns['{{PizzaCutter.docs.build_badge_link}}'] = """
.. |build_badge| image:: https://img.shields.io/travis/{{PizzaCutter.repository_slug}}/master.svg
   :target: https://travis-ci.com/{{PizzaCutter.repository_slug}}
"""

        elif self.docs_show_which_ci_badge == 'gha':
            test_link = f' <https://github.com/{self.travis_repo_slug}/actions/workflows/python-package.yml>`_, automatic daily builds and monitoring'
            self.pizza_cutter_patterns['{{PizzaCutter.docs.build_badge}}'] = '|build_badge| '
            self.pizza_cutter_patterns['{{PizzaCutter.docs.build_badge_link}}'] = """
.. |build_badge| image:: https://github.com/{{PizzaCutter.repository_slug}}/actions/workflows/python-package.yml/badge.svg
   :target: https://github.com/{{PizzaCutter.repository_slug}}/actions/workflows/python-package.yml
"""

        if l_tested_under:
            tested_under = ''.join(['tested under `', ', '.join(l_tested_under), test_link])
        else:
            tested_under = ''

        self.pizza_cutter_patterns['{{PizzaCutter.docs.test_info}}'] = ''.join([msg_code_coverage, msg_style_checking, msg_mypy_tests, tested_under])

# #############################################################################################################################################################
# Hooks
# #############################################################################################################################################################
    def pizza_cutter_hook_before_build(self):
        pass

    def pizza_cutter_hook_after_build(self):

        # check if the jupyter file is present if selected jupyter
        if self.docs_badges_with_jupiter:
            path_jupyter_file = (pathlib.Path(self.pizza_cutter_path_target_dir) / self.project_dir / self.package_name).with_suffix('.ipynb')
            if not path_jupyter_file.is_file():
                logger.warning('You selected Binder (Jupyter) Badge, but the Jupyter File is not present : "{}"'.format(path_jupyter_file))

        # create the marker file for typed packages
        if self.is_typed_package:
            (self.path_package_dir / 'py.typed').touch(exist_ok=True)
        else:
            (self.path_package_dir / 'py.typed').unlink(missing_ok=True)

        # create documentation
        import rst_include

        path_cli_module = self.path_package_dir / (self.cli_module + '.py')
        path_cli_help_rst_file = self.path_project_dir / self.docs_dir / 'commandline_help.rst'
        self.create_commandline_help_file(path_cli_module=path_cli_module,
                                          path_cli_help_rst_file=path_cli_help_rst_file,
                                          registered_shell_command=self.shell_command)

        path_rst_source_file = self.path_project_dir / self.docs_dir / 'README_template.rst'
        path_rst_target_file = self.path_project_dir / 'README.rst'
        rst_include.lib_main.rst_inc(source=path_rst_source_file, target=path_rst_target_file)
        # replace "{{\\PizzaCutter" with "{{PizzaCutter" - we use it in docs, so it will not be replaced by accident
        text = path_rst_target_file.read_text()
        text = text.replace('{{\\PizzaCutter', '{{PizzaCutter')
        path_rst_target_file.write_text(text)

        # black files if needed
        # we guess that if setup.py exists, we are in the final package
        path_setup_py = self.path_project_dir / 'setup.py'

        if path_setup_py.is_file() and self.black_auto_in_local_testscript:
            path_black = self.path_project_dir / '**/*.py'
            command = f'black {path_black}'
            subprocess.run(command, shell=True)

        if path_setup_py.is_file():
            logger.warning(f'reformatting "{path_setup_py}"')
            command = f'black {path_setup_py}'
            subprocess.run(command, shell=True)

        if self.add_github_actions is False:
            (self.path_project_dir / '.github/workflows/python-package.yml').unlink(missing_ok=True)


    # TODO: make external module in order to parse click help for sub commands / groups
    def create_commandline_help_file(self, path_cli_module: pathlib.Path, path_cli_help_rst_file: pathlib.Path, registered_shell_command: str) -> None:
        """
        creates the help text from the cli interface, by calling the cli with option -h
        and reformat that text file to rst code block format)
        """

        '''
        >>> # Setup
        >>> path_tests_dir = pathlib.Path(__file__).parent.parent / 'tests'
        >>> path_module_file = path_tests_dir / 'test_cli_help.py'
        >>> path_cli_help_rst_file = path_tests_dir / 'test_cli_help_result.rst'
    
        >>> # Test simple
        >>> create_commandline_help_file(path_module_file, path_cli_help_rst_file)
        '''

        if path_cli_module.is_file():
            command = '{sys_executable} {path_cli_module} -h'.format(sys_executable=sys.executable,
                                                                     path_cli_module=path_cli_module)
            subprocess_result = subprocess.run(command, shell=True, capture_output=True)
            # brush off backspace from output because of a bug in click, see : https://github.com/pallets/click/issues/1597
            txt_result = subprocess_result.stdout.decode('utf-8').replace('\b ', '')
            # replace the executable filename with the registered shell command
            txt_result = txt_result.replace(path_cli_module.name, registered_shell_command)
            if txt_result == '':
                txt_result = 'can not get help - probably not a proper click application'
            path_cli_help_rst_file.write_text(txt_result)
            self.reformat_txt_file_to_rst_code_block(path_source_file=path_cli_help_rst_file, path_target_file=path_cli_help_rst_file)
        else:
            logger.warning('can not find cli_module: "{path_cli_module}"'.format(path_cli_module=path_cli_module))

    # TODO: make external module in order to parse click help for sub commands / groups
    @staticmethod
    def reformat_txt_file_to_rst_code_block(path_source_file: pathlib.Path, path_target_file: pathlib.Path) -> None:
        """
        reformat a text file to rst code block format. target file can be the same as source File
        """

        '''
        >>> # Setup
        >>> path_tests_dir = pathlib.Path(__file__).parent.parent / 'tests'
        >>> path_test_file = path_tests_dir / 'txt_file_input.txt'
        >>> path_test_result = path_tests_dir / 'txt_file_result.txt'
        >>> path_test_inplace = path_tests_dir / 'txt_file_inplace.txt'
        >>> path_test_expected = path_tests_dir / 'txt_file_output_as_rst_codeblock_expected.txt'
        >>> path_test_empty_expected = path_tests_dir / 'txt_file_output_as_rst_codeblock_empty_expected.txt'
        >>> path_not_exists = path_tests_dir / 'does_not_exist.txt'
        >>> discard = shutil.copy(str(path_test_file), str(path_test_inplace))
    
        >>> # Test source <> target
        >>> reformat_txt_file_to_rst_code_block(path_source_file=path_test_file, path_target_file=path_test_result)
        >>> assert path_test_result.read_text() == path_test_expected.read_text()
    
        >>> # Test source == target
        >>> reformat_txt_file_to_rst_code_block(path_source_file=path_test_inplace, path_target_file=path_test_inplace)
        >>> assert path_test_inplace.read_text() == path_test_expected.read_text()
    
        >>> # Test source does not exist, source <> target
        >>> reformat_txt_file_to_rst_code_block(path_source_file=path_not_exists, path_target_file=path_test_result)
        >>> assert path_test_result.read_text() == path_test_empty_expected.read_text()
        >>> path_test_result.unlink()
    
        >>> # Test source does not exist, source == target
        >>> reformat_txt_file_to_rst_code_block(path_source_file=path_not_exists, path_target_file=path_not_exists)
        >>> assert path_not_exists.read_text() == path_test_empty_expected.read_text()
    
        >>> # Teardown
        >>> if path_test_result.exists(): path_test_result.unlink()
        >>> if path_test_inplace.exists(): path_test_inplace.unlink()
        >>> if path_not_exists.exists(): path_not_exists.unlink()
        '''
        path_target_file = path_target_file.resolve()
        path_source_file = path_source_file.resolve()
        if path_target_file == path_source_file:
            path_temp_file = path_target_file.parent / (path_target_file.name + '.tmp')
        else:
            path_temp_file = path_target_file

        if path_source_file.is_file():
            with open(str(path_source_file), 'r', encoding='utf-8-sig') as f_sourcefile:
                with open(str(path_temp_file), 'w', encoding='utf-8') as f_temp_file:
                    f_temp_file.write('.. code-block::\n\n')
                    for cnt, source_line in enumerate(f_sourcefile):
                        f_temp_file.write(('   ' + source_line).rstrip() + '\n')
        else:
            with open(str(path_temp_file), 'w') as f_temp_file:
                f_temp_file.write('.. code-block::\n\n    there are no commandline options\n')

        if path_target_file == path_source_file:
            if path_source_file.exists():
                path_source_file.unlink()
            path_temp_file.rename(path_source_file)


def remove_from_list(a_list, item) -> None:
    """
    remove an item from a list without error if it is not there
    """
    try:
        a_list.remove(item)
    except ValueError:
        pass

# #############################################################################################################################################################
# CLI Interface
# #############################################################################################################################################################


def main() -> None:
    import pizzacutter
    path_conf_file = pathlib.Path(__file__).resolve()
    path_template_dir = pathlib.Path(__file__).resolve().parent
    path_target_dir = pathlib.Path(__file__).resolve().parent.parent

    pizzacutter.build(path_conf_file=path_conf_file,
                      path_template_dir=path_template_dir,
                      path_target_dir=path_target_dir, allow_overwrite=True)


if __name__ == '__main__':
    main()
