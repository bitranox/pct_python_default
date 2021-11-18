# CONF

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
