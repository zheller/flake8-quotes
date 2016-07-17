import optparse
import tokenize
import warnings

import pep8

from flake8_quotes.__about__ import __version__


class QuoteChecker(object):
    name = __name__
    version = __version__

    INLINE_QUOTES = {
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

    @staticmethod
    def _register_opt(parser, *args, **kwargs):
        """
        Handler to register an option for both Flake8 3.x and 2.x.

        This is based on:
        https://github.com/PyCQA/flake8/blob/3.0.0b2/docs/source/plugin-development/cross-compatibility.rst#option-handling-on-flake8-2-and-3

        It only supports `parse_from_config` from the original function and it
        uses the `Option` object returned to get the string.
        """
        try:
            # Flake8 3.x registration
            parser.add_option(*args, **kwargs)
        except (optparse.OptionError, TypeError):
            # Flake8 2.x registration
            parse_from_config = kwargs.pop('parse_from_config', False)
            option = parser.add_option(*args, **kwargs)
            if parse_from_config:
                parser.config_options.append(option.get_opt_string().lstrip('-'))

    @classmethod
    def add_options(cls, parser):
        cls._register_opt(parser, '--quotes', action='store',
                          parse_from_config=True,
                          help='Deprecated alias for `--inline-quotes`')
        cls._register_opt(parser, '--inline-quotes', default='\'',
                          action='store', parse_from_config=True,
                          help='Quote to expect in all files (default: \')')

    @classmethod
    def parse_options(cls, options):
        if hasattr(options, 'quotes') and options.quotes is not None:
            # https://docs.python.org/2/library/warnings.html#warnings.warn
            warnings.warn('flake8-quotes has deprecated `quotes` in favor of `inline-quotes`. '
                          'Please update your configuration')
            cls.inline_quotes = cls.INLINE_QUOTES[options.quotes]
        else:
            cls.inline_quotes = cls.INLINE_QUOTES[options.inline_quotes]

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

            # Remove any prefixes in strings like `u` from `u"foo"`
            # DEV: `last_quote_char` is 1 character, even for multiline strings
            #   `"foo"`   -> `"foo"`
            #   `b"foo"`  -> `"foo"`
            #   `br"foo"` -> `"foo"`
            #   `b"""foo"""` -> `"""foo"""`
            last_quote_char = token.string[-1]
            first_quote_index = token.string.index(last_quote_char)
            unprefixed_string = token.string[first_quote_index:]

            if not unprefixed_string.startswith(self.inline_quotes['bad_single']):
                # ignore strings that do not start with our quotes
                continue

            if unprefixed_string.startswith(self.inline_quotes['bad_multiline']):
                # ignore multiline strings
                continue

            if self.inline_quotes['good_single'] in unprefixed_string:
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
