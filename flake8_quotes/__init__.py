import optparse
import tokenize
import warnings

import pep8

from flake8_quotes.__about__ import __version__


class QuoteChecker(object):
    name = __name__
    version = __version__

    INLINE_QUOTES = ['"', "'"]
    MULTILINE_QUOTES = ['"""', "'''"]

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
                          parse_from_config=True, choices=cls.INLINE_QUOTES,
                          help='Deprecated alias for `--inline-quotes`')
        cls._register_opt(parser, '--inline-quotes', default='\'',
                          action='store', parse_from_config=True,
                          choices=cls.INLINE_QUOTES,
                          help='Quote to expect in all files (default: \')')
        cls._register_opt(parser, '--multiline-quotes', action='store',
                          choices=cls.INLINE_QUOTES,
                          help='Quote to expect in all files (default same as inline quote)')

    @classmethod
    def parse_options(cls, options):
        if hasattr(options, 'quotes') and options.quotes is not None:
            # https://docs.python.org/2/library/warnings.html#warnings.warn
            warnings.warn('flake8-quotes has deprecated `quotes` in favor of `inline-quotes`. '
                          'Please update your configugration')
            options.inline_quotes = options.quotes

        cls.inline_quotes = options.inline_quotes
        if options.multiline_quotes is None:
            options.multiline_quotes = options.inline_quotes
        # assume that multiline quotes are all 3x singleline quotes
        cls.multiline_quotes = options.multiline_quotes * 3

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

    def complain(self, unprefixed_string, is_multiline):
        quote_configured = self.multiline_quotes if is_multiline else self.inline_quotes
        quote_used = unprefixed_string[:3 if is_multiline else 1]
        # If the quote used is the wanted one, do not complain
        if quote_used == quote_configured:
            return False
        # If the wanted quote is in the unprefixed string, do not complain
        elif quote_configured in unprefixed_string:
            return False
        # Otherwise it could use the other quote
        else:
            return True

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

            err = False
            if unprefixed_string[:3] in self.MULTILINE_QUOTES:
                if self.complain(unprefixed_string, True):
                    err = 'Q001 Wrong multiline quote style used'
            else:
                if self.complain(unprefixed_string, False):
                    err = 'Q000 Remove bad quotes.'

            # Nothing to complain
            if err is False:
                continue

            start_row, start_col = token.start
            yield {
                'message': err,
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
