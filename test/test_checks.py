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
        self.assertRegex(
            stdout_lines[0],
            b'stdin:1:(24|25): Q000 Double quotes found but single quotes preferred')
        self.assertRegex(
            stdout_lines[1],
            b'stdin:2:(24|25): Q000 Double quotes found but single quotes preferred')
        self.assertRegex(
            stdout_lines[2],
            b'stdin:3:(24|25): Q000 Double quotes found but single quotes preferred')


class DoublesTestChecks(TestCase):
    def setUp(self):
        class DoublesOptions():
            inline_quotes = "'"
            multiline_quotes = "'"
        QuoteChecker.parse_options(DoublesOptions)

    def test_multiline_string(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_multiline_string.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [
            {'col': 4, 'line': 1, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
        ])

    def test_multiline_string_using_lines(self):
        with open(get_absolute_path('data/doubles_multiline_string.py')) as f:
            lines = f.readlines()
        doubles_checker = QuoteChecker(None, lines=lines)
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [
            {'col': 4, 'line': 1, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
        ])

    def test_wrapped(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_wrapped.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [])

    def test_doubles(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [
            {'col': 24, 'line': 1, 'message': 'Q000 Double quotes found but single quotes preferred'},
            {'col': 24, 'line': 2, 'message': 'Q000 Double quotes found but single quotes preferred'},
            {'col': 24, 'line': 3, 'message': 'Q000 Double quotes found but single quotes preferred'},
        ])

    def test_noqa_doubles(self):
        checker = QuoteChecker(None, get_absolute_path('data/doubles_noqa.py'))
        self.assertEqual(list(checker.run()), [])

    def test_escapes(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_escaped.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [
            {'col': 25, 'line': 1, 'message': 'Q003 Change outer quotes to avoid escaping inner quotes'},
        ])

    def test_escapes_allowed(self):
        class Options():
            inline_quotes = "'"
            avoid_escape = False
        QuoteChecker.parse_options(Options)

        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_escaped.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [])


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
            {'col': 24, 'line': 1, 'message': 'Q000 Double quotes found but single quotes preferred'},
            {'col': 24, 'line': 2, 'message': 'Q000 Double quotes found but single quotes preferred'},
            {'col': 24, 'line': 3, 'message': 'Q000 Double quotes found but single quotes preferred'},
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
            {'col': 4, 'line': 1, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
        ])

    def test_wrapped(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_wrapped.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [])

    def test_singles(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [
            {'col': 24, 'line': 1, 'message': 'Q000 Single quotes found but double quotes preferred'},
            {'col': 24, 'line': 2, 'message': 'Q000 Single quotes found but double quotes preferred'},
            {'col': 24, 'line': 3, 'message': 'Q000 Single quotes found but double quotes preferred'},
        ])

    def test_noqa_singles(self):
        checker = QuoteChecker(None, get_absolute_path('data/singles_noqa.py'))
        self.assertEqual(list(checker.run()), [])

    def test_escapes(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_escaped.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [
            {'col': 25, 'line': 1, 'message': 'Q003 Change outer quotes to avoid escaping inner quotes'},
        ])

    def test_escapes_allowed(self):
        class Options():
            inline_quotes = '"'
            avoid_escape = False
        QuoteChecker.parse_options(Options)

        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_escaped.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [])


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
            {'col': 24, 'line': 1, 'message': 'Q000 Single quotes found but double quotes preferred'},
            {'col': 24, 'line': 2, 'message': 'Q000 Single quotes found but double quotes preferred'},
            {'col': 24, 'line': 3, 'message': 'Q000 Single quotes found but double quotes preferred'},
        ])


class MultilineTestChecks(TestCase):
    def test_singles(self):
        class Options():
            inline_quotes = "'"
            multiline_quotes = '"'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 10, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
        ])

    def test_singles_alias(self):
        class Options():
            inline_quotes = 'single'
            multiline_quotes = 'double'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 10, 'message': 'Q001 Single quote multiline found but double quotes preferred'},
        ])

    def test_doubles(self):
        class Options():
            inline_quotes = '"'
            multiline_quotes = "'"
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 1, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
        ])

    def test_doubles_alias(self):
        class Options():
            inline_quotes = 'double'
            multiline_quotes = 'single'
        QuoteChecker.parse_options(Options)

        multiline_checker = QuoteChecker(None, filename=get_absolute_path('data/multiline_string.py'))
        self.assertEqual(list(multiline_checker.get_quotes_errors(multiline_checker.get_file_contents())), [
            {'col': 4, 'line': 1, 'message': 'Q001 Double quote multiline found but single quotes preferred'},
        ])


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
