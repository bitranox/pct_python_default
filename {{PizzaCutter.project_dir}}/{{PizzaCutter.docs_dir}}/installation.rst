- Before You start, its highly recommended to update pip and setup tools:


.. code-block::

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools


{{PizzaCutter.docs.include_installation_via_pypi}}

- to install the latest version from github via pip:


.. code-block::

    python -m pip install --upgrade git+https://github.com/{{PizzaCutter.repository_slug}}.git


- include it into Your requirements.txt:

.. code-block::

    # Insert following line in Your requirements.txt:
    {{PizzaCutter.docs.pypi_requirements}}{{PizzaCutter.option.delete_line_if_empty}}
    # for the latest development version :
    {{PizzaCutter.repository}} @ git+https://github.com/{{PizzaCutter.repository_slug}}.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version from source code:

.. code-block::

    # cd ~
    $ git clone https://github.com/{{PizzaCutter.repository_slug}}.git
    $ cd {{PizzaCutter.repository}}
    python setup.py install


.. include:: ./installation_via_makefile.rst
