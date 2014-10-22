import re
from flake8_quotes import __version__


def check_quotes(logical_line):
    """Raise lint error when using " instead of '."""
    # if there is no double quote sign there's nothing to do
    if logical_line.find('"') == -1:
        return

    # if it's a comment logical_line ignore it
    if logical_line.strip().startswith('#'):
        return

    # if it's a multilogical_line string, it is ok to have doublequotes
    if logical_line.find('"""') != -1:
        return

    # ignore double quotes wrapped in singlequotes
    singles = re.match(r"'(.*)'", logical_line)
    if singles and logical_line.find('"') != -1:
        return

    double_quotes = logical_line.find('"')
    if double_quotes:
        yield double_quotes + 1, 'Q000 Remove Double quotes.'


check_quotes.name = name ='flake8-quotes'
check_quotes.version = __version__
