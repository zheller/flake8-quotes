import tokenize

import pep8
import pkg_resources


__version__ = pkg_resources.get_distribution('flake8_quotes').version


class QuoteChecker(object):
    name = __name__
    version = __version__

    QUOTES = {
        # When user wants only single quotes
        '\'': {
            'good_single': '\'',
            'good_multiline': '\'\'\'',
            'bad_single': '"',
            'bad_multiline': '"""',
        },
        '"': {
            'good_single': '"',
            'good_multiline': '"""',
            'bad_single': '\'',
            'bad_multiline': '\'\'\'',
        },
    }

    def __init__(self, tree, filename='(none)', builtins=None):
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        parser.add_option('--quotes', default='\'', action='store',
                          help='Quote to expect in all files (default: \')')
        parser.config_options.append('quotes')

    @classmethod
    def parse_options(cls, options):
        cls.quotes = cls.QUOTES[options.quotes]

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

            if not token.string.startswith(self.quotes['bad_single']):
                # ignore strings that do not start with our quotes
                continue

            if token.string.startswith(self.quotes['bad_multiline']):
                # ignore multiline strings
                continue

            if self.quotes['good_single'] in token.string:
                # ignore alternate quotes wrapped in our quotes (e.g. `'` in `"it's"`)
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
