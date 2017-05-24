import tokenize

from flake8_quotes import Token, get_docstring_tokens

from flake8_quotes import QuoteChecker
import os
import subprocess
from unittest import TestCase


class TestChecks(TestCase):
    def test_get_noqa_lines(self):
        checker = QuoteChecker(None, filename=get_absolute_path('data/no_qa.py'))
        self.assertEqual(checker.get_noqa_lines(checker.get_file_contents()), [2])


class TestFlake8Stdin(TestCase):
    def test_stdin(self):
        """Test using stdin."""
        filepath = get_absolute_path('data/doubles.py')
        with open(filepath, 'rb') as f:
            p = subprocess.Popen(['flake8', '--select=Q', '-'], stdin=f,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()

        stdout_lines = stdout.splitlines()
        self.assertEqual(stderr, b'')
        self.assertEqual(len(stdout_lines), 3)
        self.assertRegexpMatches(stdout_lines[0], b'stdin:1:(24|25): Q000 Remove bad quotes.')
        self.assertRegexpMatches(stdout_lines[1], b'stdin:2:(24|25): Q000 Remove bad quotes.')
        self.assertRegexpMatches(stdout_lines[2], b'stdin:3:(24|25): Q000 Remove bad quotes.')


class DoublesTestChecks(TestCase):
    def setUp(self):
        class DoublesOptions():
            inline_quotes = '\''
            multiline_quotes = '\''
        QuoteChecker.parse_options(DoublesOptions)

    def test_multiline_string(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_multiline_string.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [
            {'col': 4, 'line': 1, 'message': 'Q001 Remove bad quotes from multiline string.'},
        ])

    def test_wrapped(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_wrapped.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [])

    def test_doubles(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [
            {'col': 24, 'line': 1, 'message': 'Q000 Remove bad quotes.'},
            {'col': 24, 'line': 2, 'message': 'Q000 Remove bad quotes.'},
            {'col': 24, 'line': 3, 'message': 'Q000 Remove bad quotes.'},
        ])

    def test_noqa_doubles(self):
        checker = QuoteChecker(None, get_absolute_path('data/doubles_noqa.py'))
        self.assertEqual(list(checker.run()), [])


class DoublesAliasTestChecks(TestCase):
    def setUp(self):
        class DoublesAliasOptions():
            inline_quotes = 'single'
            multiline_quotes = 'single'
        QuoteChecker.parse_options(DoublesAliasOptions)

    def test_doubles(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_wrapped.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [])

        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [
            {'col': 24, 'line': 1, 'message': 'Q000 Remove bad quotes.'},
            {'col': 24, 'line': 2, 'message': 'Q000 Remove bad quotes.'},
            {'col': 24, 'line': 3, 'message': 'Q000 Remove bad quotes.'},
        ])


class SinglesTestChecks(TestCase):
    def setUp(self):
        class SinglesOptions():
            inline_quotes = '"'
            multiline_quotes = '"'
        QuoteChecker.parse_options(SinglesOptions)

    def test_multiline_string(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_multiline_string.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [
            {'col': 4, 'line': 1, 'message': 'Q001 Remove bad quotes from multiline string.'},
        ])

    def test_wrapped(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_wrapped.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [])

    def test_singles(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [
            {'col': 24, 'line': 1, 'message': 'Q000 Remove bad quotes.'},
            {'col': 24, 'line': 2, 'message': 'Q000 Remove bad quotes.'},
            {'col': 24, 'line': 3, 'message': 'Q000 Remove bad quotes.'},
        ])

    def test_noqa_singles(self):
        checker = QuoteChecker(None, get_absolute_path('data/singles_noqa.py'))
        self.assertEqual(list(checker.run()), [])


class SinglesAliasTestChecks(TestCase):
    def setUp(self):
        class SinglesAliasOptions():
            inline_quotes = 'double'
            multiline_quotes = 'double'
        QuoteChecker.parse_options(SinglesAliasOptions)

    def test_singles(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_wrapped.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [])

        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [
            {'col': 24, 'line': 1, 'message': 'Q000 Remove bad quotes.'},
            {'col': 24, 'line': 2, 'message': 'Q000 Remove bad quotes.'},
            {'col': 24, 'line': 3, 'message': 'Q000 Remove bad quotes.'},
        ])


class MultilineTestChecks(TestCase):
    def test_singles(self):
        class Options():
            inline_quotes = '\''
            multiline_quotes = '"'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 10, 'message': 'Q001 Remove bad quotes from multiline string.'},
        ])

    def test_singles_alias(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'double'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None,
                                         filename=get_absolute_path('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 10, 'message': 'Q001 Remove bad quotes from multiline string.'},
        ])

    def test_doubles(self):
        class Options():
            inline_quotes = '"'
            multiline_quotes = '\''
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 1, 'message': 'Q001 Remove bad quotes from multiline string.'},
        ])

    def test_doubles_alias(self):
        class Options():
            inline_quotes = 'double'
            multiline_quotes = 'single'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 1, 'message': 'Q001 Remove bad quotes from multiline string.'},
        ])


class DocstringTestChecks(TestCase):
    def test(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'single'
            docstring_quotes = 'double'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/docstring_doubles.py'))
        self.assertEquals(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [])


class GetDocstringTokensTests(TestCase):
    def _get_docstring_tokens(self, filename):
        f = open(get_absolute_path(filename), 'r')
        tokens = [Token(t) for t in tokenize.generate_tokens(f.readline)]
        return get_docstring_tokens(tokens)

    def test_get_docstring_tokens_absent(self):
        self.assertEqual(self._get_docstring_tokens('data/doubles.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/doubles_multiline_string.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/doubles_noqa.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/doubles_wrapped.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/multiline_string.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/no_qa.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/singles.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/singles_multiline_string.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/singles_noqa.py'), set())
        self.assertEqual(self._get_docstring_tokens('data/singles_wrapped.py'), set())

    def test_get_docstring_tokens(self):
        f = open(get_absolute_path('data/docstring_doubles.py'), 'r')
        tokens = [Token(t) for t in tokenize.generate_tokens(f.readline)]
        docstring_tokens = get_docstring_tokens(tokens)
        self.assertEqual(docstring_tokens, {tokens[1], tokens[12], tokens[26]})


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
