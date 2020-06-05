import tokenize
import warnings

from flake8_quotes.__about__ import __version__
from flake8_quotes.docstring_detection import get_docstring_tokens


class QuoteChecker:
    name = __name__
    version = __version__

    INLINE_QUOTES = {
        # When user wants only single quotes
        "'": {
            'good_single': "'",
            'bad_single': '"',
        },
        # When user wants only double quotes
        '"': {
            'good_single': '"',
            'bad_single': "'",
        },
    }
    # Provide aliases for Windows CLI support
    #   https://github.com/zheller/flake8-quotes/issues/49
    INLINE_QUOTES['single'] = INLINE_QUOTES["'"]
    INLINE_QUOTES['double'] = INLINE_QUOTES['"']

    MULTILINE_QUOTES = {
        "'": {
            'good_multiline': "'''",
            'good_multiline_ending': '\'"""',
            'bad_multiline': '"""',
        },
        '"': {
            'good_multiline': '"""',
            'good_multiline_ending': '"\'\'\'',
            'bad_multiline': "'''",
        },
    }
    # Provide Windows CLI and multi-quote aliases
    MULTILINE_QUOTES['single'] = MULTILINE_QUOTES["'"]
    MULTILINE_QUOTES['double'] = MULTILINE_QUOTES['"']
    MULTILINE_QUOTES["'''"] = MULTILINE_QUOTES["'"]
    MULTILINE_QUOTES['"""'] = MULTILINE_QUOTES['"']

    DOCSTRING_QUOTES = {
        "'": {
            'good_docstring': "'''",
            'bad_docstring': '"""',
        },
        '"': {
            'good_docstring': '"""',
            'bad_docstring': "'''",
        },
    }
    # Provide Windows CLI and docstring-quote aliases
    DOCSTRING_QUOTES['single'] = DOCSTRING_QUOTES["'"]
    DOCSTRING_QUOTES['double'] = DOCSTRING_QUOTES['"']
    DOCSTRING_QUOTES["'''"] = DOCSTRING_QUOTES["'"]
    DOCSTRING_QUOTES['"""'] = DOCSTRING_QUOTES['"']

    @classmethod
    def add_options(cls, option_manager):
        option_manager.add_option('--quotes', action='store',
                                  parse_from_config=True, type='choice',
                                  choices=sorted(cls.INLINE_QUOTES.keys()),
                                  help='Deprecated alias for `--inline-quotes`')
        option_manager.add_option('--inline-quotes', default="'",
                                  action='store', parse_from_config=True, type='choice',
                                  choices=sorted(cls.INLINE_QUOTES.keys()),
                                  help="Quote to expect in all files (default: ')")
        option_manager.add_option('--multiline-quotes', default=None, action='store',
                                  parse_from_config=True, type='choice',
                                  choices=sorted(cls.MULTILINE_QUOTES.keys()),
                                  help='Quote to expect in all files (default: """)')
        option_manager.add_option('--docstring-quotes', default=None, action='store',
                                  parse_from_config=True, type='choice',
                                  choices=sorted(cls.DOCSTRING_QUOTES.keys()),
                                  help='Quote to expect in all files (default: """)')
        option_manager.add_option('--avoid-escape', default=None, action='store_true',
                                  parse_from_config=True,
                                  help='Avoiding escaping same quotes in inline strings (enabled by default)')
        option_manager.add_option('--no-avoid-escape', dest='avoid_escape', default=None, action='store_false',
                                  parse_from_config=False,
                                  help='Disable avoiding escaping same quotes in inline strings')

    @classmethod
    def parse_options(cls, options):
        # Define our default config
        # cls.config = {good_single: ', good_multiline: ''', bad_single: ", bad_multiline: """}
        cls.config = {}
        cls.config.update(cls.INLINE_QUOTES["'"])
        cls.config.update(cls.MULTILINE_QUOTES['"""'])
        cls.config.update(cls.DOCSTRING_QUOTES['"""'])

        # If `options.quotes` was specified, then use it
        if hasattr(options, 'quotes') and options.quotes is not None:
            # https://docs.python.org/2/library/warnings.html#warnings.warn
            warnings.warn('flake8-quotes has deprecated `quotes` in favor of `inline-quotes`. '
                          'Please update your configuration')
            cls.config.update(cls.INLINE_QUOTES[options.quotes])
        # Otherwise, use the supported `inline_quotes`
        else:
            # cls.config = {good_single: ', good_multiline: """, bad_single: ", bad_multiline: '''}
            #   -> {good_single: ", good_multiline: """, bad_single: ', bad_multiline: '''}
            cls.config.update(cls.INLINE_QUOTES[options.inline_quotes])

        # If multiline quotes was specified, overload our config with those options
        if hasattr(options, 'multiline_quotes') and options.multiline_quotes is not None:
            # cls.config = {good_single: ', good_multiline: """, bad_single: ", bad_multiline: '''}
            #   -> {good_single: ', good_multiline: ''', bad_single: ", bad_multiline: """}
            cls.config.update(cls.MULTILINE_QUOTES[options.multiline_quotes])

        # If docstring quotes was specified, overload our config with those options
        if hasattr(options, 'docstring_quotes') and options.docstring_quotes is not None:
            cls.config.update(cls.DOCSTRING_QUOTES[options.docstring_quotes])

        # If avoid escaped specified, add to config
        if hasattr(options, 'avoid_escape') and options.avoid_escape is not None:
            cls.config.update({'avoid_escape': options.avoid_escape})
        else:
            cls.config.update({'avoid_escape': True})

    def __init__(self, logical_line, previous_logical, tokens):
        self.line = logical_line
        self.tokens = tokens

        # Generate `readline()` matching interface for `tokenize.tokenize` and pass it in
        #   https://docs.python.org/3/library/tokenize.html#tokenize.tokenize
        previous_logical_readline_fn = (lambda L=iter([previous_logical.encode('utf-8')]): next(L))
        prev_tokens = tokenize.tokenize(previous_logical_readline_fn)
        self.docstring_tokens = get_docstring_tokens(prev_tokens, self.tokens)

    def __iter__(self):
        for token in self.tokens:
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
            prefix = token.string[:first_quote_index].lower()
            unprefixed_string = token.string[first_quote_index:]

            # Determine if our string is multiline-based
            #   "foo"[0] * 3 = " * 3 = """
            #   "foo"[0:3] = "fo
            #   """foo"""[0:3] = """
            is_docstring = token in self.docstring_tokens
            is_multiline_string = unprefixed_string[0] * 3 == unprefixed_string[0:3]

            # If our string is a docstring
            # DEV: Docstring quotes must come before multiline quotes as it can as a multiline quote
            if is_docstring:
                if self.config['good_docstring'] in unprefixed_string:
                    continue

                yield (token.start, 'Q002 Remove bad quotes from docstring')
            # Otherwise if our string is multiline
            elif is_multiline_string:
                # If our string is or containing a known good string, then ignore it
                #   (""")foo""" -> good (continue)
                #   '''foo(""")''' -> good (continue)
                #   (''')foo''' -> possibly bad
                if self.config['good_multiline'] in unprefixed_string:
                    continue

                # If our string ends with a known good ending, then ignore it
                #   '''foo("''') -> good (continue)
                #     Opposite, """foo"""", would break our parser (cannot handle """" ending)
                if unprefixed_string.endswith(self.config['good_multiline_ending']):
                    continue

                # Output our error
                yield (token.start, 'Q001 Remove bad quotes from multiline string')
            # Otherwise (string is inline quote)
            else:
                #   'This is a string'       -> Good
                #   'This is a "string"'     -> Good
                #   'This is a \"string\"'   -> Good
                #   'This is a \'string\''   -> Bad (Q003)  Escaped inner quotes
                #   '"This" is a \'string\'' -> Good        Changing outer quotes would not avoid escaping
                #   "This is a string"       -> Bad (Q000)
                #   "This is a 'string'"     -> Good        Avoids escaped inner quotes
                #   "This is a \"string\""   -> Bad (Q000)
                #   "\"This\" is a 'string'" -> Good

                string_contents = unprefixed_string[1:-1]

                # If string preferred type, check for escapes
                if last_quote_char == self.config['good_single']:
                    if not self.config['avoid_escape'] or 'r' in prefix:
                        continue
                    if (self.config['good_single'] in string_contents and
                            not self.config['bad_single'] in string_contents):
                        yield (token.start, 'Q003 Change outer quotes to avoid escaping inner quotes')
                    continue

                # If not preferred type, only allow use to avoid escapes.
                if not self.config['good_single'] in string_contents:
                    yield (token.start, 'Q000 Remove bad quotes')
