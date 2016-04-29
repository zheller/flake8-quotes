import tokenize

import pep8

from flake8_quotes.__about__ import __version__


class QuoteChecker(object):
    name = __name__
    version = __version__

    QUOTES = {
        # Allow single quotes
        # Fail on double quotes
        '\'': {
            'allow': '\'',
            'fail': '"',
        },

        # Allow double quotes
        # Fail on single quotes
        '"': {
            'allow': '"',
            'fail': '\'',
        },
    }

    MULTILINE_QUOTES = {
        # Allow single multiline quotes
        # Fail on double multiline quotes
        '\'': {
            'allow': '\'\'\'',
            'fail': '"""'
        },

        # Allow double multiline quotes
        # Fail on single multiline quotes
        '"': {
            'allow': '"""',
            'fail': '\'\'\''
        }
    }

    def __init__(self, tree, filename='(none)', builtins=None):
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--quotes', default='\'', action='store',
                          help='Quote to expect in all files (default: \')')
        parser.add_option('--multiline-quotes', default='\'', action='store',
                          help='Multiline quote to expect in all files (default: \')')
        parser.config_options.extend(['quotes', 'multiline_quotes'])

    @classmethod
    def parse_options(cls, options):
        if hasattr(options, 'multiline_quotes'):
            multiline_quotes = options.multiline_quotes
        else:
            multiline_quotes = options.quotes

        cls.quotes = cls.QUOTES[options.quotes]
        cls.multiline_quotes = cls.MULTILINE_QUOTES[multiline_quotes]

    def get_file_contents(self):
        if self.filename in ('stdin', '-', None):
            return pep8.stdin_get_value().splitlines(True)
        else:
            return pep8.readlines(self.filename)

    def run(self):
        file_contents = self.get_file_contents()

        noqa_line_numbers = self.get_noqa_lines(file_contents)
        errors = self.get_quotes_errors(file_contents)

        for error in errors:
            if error.get('line') not in noqa_line_numbers:
                yield (error.get('line'), error.get('col'), error.get('message'), type(self))

    def get_noqa_lines(self, file_contents):
        tokens = [Token(t) for t in tokenize.generate_tokens(lambda L=iter(file_contents): next(L))]
        return [token.start_row
                for token in tokens
                if token.type == tokenize.COMMENT and token.string.endswith('noqa')]

    def get_quotes_errors(self, file_contents):
        tokens = [Token(t) for t in tokenize.generate_tokens(lambda L=iter(file_contents): next(L))]
        for token in tokens:

            if token.type != tokenize.STRING:
                # ignore non strings
                continue

            if not token.string.startswith(self.quotes['fail']) and not token.string.startswith(self.multiline_quotes['fail']):
                # ignore strings that do not start with our quotes (both single and multiline)
                continue

            if self.quotes['allow'] in token.string:
                # ignore quotes wrapped in our quotes (e.g. `'` in `"it's"`)
                continue

            if self.multiline_quotes['allow'] in token.string:
                # ignore multiline quotes wrapped in our quotes
                continue

            start_row, start_col = token.start
            yield {
                'message': 'Q000 Remove bad quotes.',
                'line': start_row,
                'col': start_col,
            }


class Token:
    '''Python 2 and 3 compatible token'''
    def __init__(self, token):
        self.token = token

    @property
    def type(self):
        return self.token[0]

    @property
    def string(self):
        return self.token[1]

    @property
    def start(self):
        return self.token[2]

    @property
    def start_row(self):
        return self.token[2][0]

    @property
    def start_col(self):
        return self.token[2][1]