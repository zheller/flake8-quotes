from sys import stdin
import tokenize


__version__ = '0.0.2'


class DoubleQuoteChecker(object):
    name = __name__
    version = __version__

    def __init__(self, tree, filename='(none)', builtins=None):
        self.file = (filename == 'stdin' and stdin) or filename

    def run(self):
        if self.file == stdin:
            file_contents = self.file
        else:
            with open(self.file, 'r') as file_to_check:
                file_contents = file_to_check.readlines()

        noqa_line_numbers = get_noqa_lines(file_contents)
        errors = get_double_quotes_errors(file_contents)

        for error in errors:
            if error.get('line') not in noqa_line_numbers:
                yield (error.get('line'), error.get('col'), error.get('message'), type(self))


def get_noqa_lines(file_contents):
    tokens = tokenize.generate_tokens(lambda L=iter(file_contents): next(L))
    return [token.start[0]
            for token in tokens
            if token.type == tokenize.COMMENT and token.string.endswith('noqa')]


def get_double_quotes_errors(file_contents):
    tokens = tokenize.generate_tokens(lambda L=iter(file_contents): next(L))
    for token in tokens:
        if token.type != tokenize.STRING:
            # ignore non strings
            continue

        if not token.string.startswith('"'):
            # ignore strings that do not start with doubles
            continue

        if token.string.startswith('"""'):
            # ignore multiline strings
            continue

        if "'" in token.string:
            # ignore singles wrapped in doubles
            continue

        start_row, start_col = token.start
        yield {
            'message': 'Q000 Remove Double quotes.',
            'line': start_row,
            'col': start_col
        }
