import subprocess

from flake8_quotes import QuoteChecker
import os
from unittest import expectedFailure, TestCase


class TestChecks(TestCase):
    def test_get_noqa_lines(self):
        checker = QuoteChecker(None, filename=get_absolute_path('data/no_qa.py'))
        self.assertEqual(checker.get_noqa_lines(checker.get_file_contents()), [2])


class TestFlake8Stdin(TestCase):

    @expectedFailure
    def test_stdin(self):
        """Test using stdin."""
        filename = get_absolute_path('data/doubles.py')
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf8'
        with open(filename, 'rb') as f:
            # For some reason using "--select=Q" did suppress all outputs, so
            # the result might contain non flake_quotes related errors
            p = subprocess.Popen(['flake8', '-'], stdin=f, env=env,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()

        out = out.decode('utf8').splitlines()
        self.assertFalse(err)
        self.assertEqual(out, [
            'stdin:1:25: Q000 Remove bad quotes.',
            'stdin:2:25: Q000 Remove bad quotes.',
            'stdin:3:25: Q000 Remove bad quotes.',
        ])


class DoublesTestChecks(TestCase):
    def setUp(self):
        class DoublesOptions():
            inline_quotes = '\''
        QuoteChecker.parse_options(DoublesOptions)

    def test_multiline_string(self):
        doubles_checker = QuoteChecker(None, filename=get_absolute_path('data/doubles_multiline_string.py'))
        self.assertEqual(list(doubles_checker.get_quotes_errors(doubles_checker.get_file_contents())), [])

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


class SinglesTestChecks(TestCase):
    def setUp(self):
        class SinglesOptions():
            inline_quotes = '"'
        QuoteChecker.parse_options(SinglesOptions)

    def test_multiline_string(self):
        singles_checker = QuoteChecker(None, filename=get_absolute_path('data/singles_multiline_string.py'))
        self.assertEqual(list(singles_checker.get_quotes_errors(singles_checker.get_file_contents())), [])

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


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
