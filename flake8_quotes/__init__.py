import tokenize

import pep8

from flake8_quotes.__about__ import __version__


class QuoteChecker(object):
    name = __name__
    version = __version__

    INLINE_QUOTES = {
        # When user wants only single quotes
        '\'': {
            'good': '\'',
            'bad': '"',
        },

        # When user wants only double quotes
        '"': {
            'good': '"',
            'bad': '\'',
        },
    }

    MULTILINE_QUOTES = {
        # When user wants only single multiline quotes
        '\'': {
            'good': '\'\'\'',
            'bad': '"""'
        },

        # When user wants only double multiline quotes
        '"': {
            'good': '"""',
            'bad': '\'\'\''
        }
    }

    def __init__(self, tree, filename='(none)', builtins=None):
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--quotes', default='\'', action='store', dest='inline_quotes',
                          help='Quote to expect in all files (default: \')')
        parser.add_option('--multiline-quotes', action='store',
                          help='Multiline quote to expect in all files (disabled by default)')
        parser.config_options.extend(['quotes', 'multiline_quotes'])

    @classmethod
    def parse_options(cls, options):
        multiline_ignored = True

        if hasattr(options, 'multiline_quotes'):
            multiline_quotes = options.multiline_quotes

            if multiline_quotes is None:
                multiline_quotes = options.inline_quotes
            else:
                multiline_ignored = False
        else:
            multiline_quotes = options.inline_quotes

        cls.inline_quotes = cls.INLINE_QUOTES[options.inline_quotes]
        cls.multiline_quotes = cls.MULTILINE_QUOTES[multiline_quotes]
        cls.multiline_ignored = multiline_ignored

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

            if not token.string.startswith(self.inline_quotes['bad']) and not token.string.startswith(self.multiline_quotes['bad']):
                # ignore strings that do not start with our quotes (both single and multiline)
                continue

            if self.multiline_ignored and any([token.string.startswith(value) for value in self.multiline_quotes.values()]):
                # ignore any type of multiline if multilines are being ignored
                continue

            if self.inline_quotes['good'] in token.string:
                # ignore quotes wrapped in our quotes (e.g. `'` in `"it's"`)
                continue

            if self.multiline_quotes['good'] in token.string:
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
