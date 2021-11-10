# if doctest or pytest is running, set paths accordingly
from . import __init__boot__   # noqa

# put Your imports here

# this needs to be after Your imports, otherwise we would create circular import on the cli script,
# which is reading some values for the __init__conf__
from . import __init__conf__
__title__ = __init__conf__.title
__version__ = __init__conf__.version
__name__ = __init__conf__.name
__url__ = __init__conf__.url
__author__ = __init__conf__.author
__author_email__ = __init__conf__.author_email
__shell_command__ = __init__conf__.shell_command
