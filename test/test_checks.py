import flake8_quotes
import os
from unittest import TestCase


class TestChecks(TestCase):

    def test_get_noqa_lines(self):
        self.assertEqual(flake8_quotes.get_noqa_lines(get_file_contents('data/no_qa.py')), [2])

    def test_multiline_string(self):
        self.assertEqual(list(flake8_quotes.get_double_quotes_errors(get_file_contents('data/multiline_string.py'))), [])

    def test_wrapped(self):
        self.assertEqual(list(flake8_quotes.get_double_quotes_errors(get_file_contents('data/wrapped.py'))), [])

    def test_doubles(self):
        self.assertEqual(list(flake8_quotes.get_double_quotes_errors(get_file_contents('data/doubles.py'))), [
            {'col': 24, 'line': 1, 'message': 'Q000 Remove Double quotes.'}
        ])

    def test_noqua_doubles(self):
        checker = flake8_quotes.DoubleQuoteChecker(None, get_absolute_path('data/doubles_noqa.py'))
        self.assertEqual(list(checker.run()), [])


def get_file_contents(filepath):
    with open(get_absolute_path(filepath), 'r') as content_file:
        return content_file.readlines()


def get_absolute_path(filepath):
    return os.path.join(os.path.dirname(__file__), filepath)
